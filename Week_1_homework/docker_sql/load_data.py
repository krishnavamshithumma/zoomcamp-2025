import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    additional_url = params.additional_url  # New URL for the additional file

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    # Download the primary CSV file
    os.system(f"wget {url} -O {csv_name}")

    # Download the additional CSV file
    if additional_url:
        additional_csv_name = 'output_taxi_zone.csv'
        os.system(f"wget {additional_url} -O {additional_csv_name}")
        
        # Load the additional CSV into DataFrame and upload to the database
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
        df_zones = pd.read_csv(additional_csv_name)
        df_zones.to_sql(name='zones', con=engine, if_exists='replace', index=False)
        print("Additional data (zones) successfully uploaded to the database.")

    # Create the SQLAlchemy engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Process and upload the first CSV file in chunks
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    # Read the first chunk
    df = next(df_iter)

    # Convert datetime columns
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    # Write the first chunk to the database
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

    while True:
        try:
            t_start = time()
            
            df = next(df_iter)

            # Convert datetime columns
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

            # Write the chunk to the database
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

            t_end = time()
            print('Inserted another chunk, took %.3f seconds' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the primary csv file')
    parser.add_argument('--additional_url', required=False, help='url of the additional csv file (optional)')

    args = parser.parse_args()

    main(args)
