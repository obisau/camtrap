from frictionless import Resource, Dialect, describe, Package, validate
import pandas as pd
import argparse
from datetime import datetime, timedelta
from pprint import pprint
from pathlib import Path
from urllib.request import urlopen
import json
import math


def find_resource(folder_path, resource_type):
    resource_path = None
    file_name_mapping = {
        "metadata": "2019-08-29_Ningaloo.Marine.Park.Commonwealth_stereo-BRUVs_Metadata.csv",
        "movieseq": "2019-08-29_Ningaloo.Marine.Park.Commonwealth_stereo-BRUVs_MovieSeq.txt",
        "lengths": "2019-08-29_Ningaloo.Marine.Park.Commonwealth_stereo-BRUVs_Lengths.txt",
        "points": "2019-08-29_Ningaloo.Marine.Park.Commonwealth_stereo-BRUVs_Points.txt"
    }

    if resource_type in file_name_mapping:
        resource_path = Path(folder_path) / file_name_mapping[resource_type]

    return resource_path


def read_schema(schema_name, version):
    schema_urls = {
        "deployments": f"https://raw.githubusercontent.com/tdwg/camtrap-dp/{version}/deployments-table-schema.json",
        "media": f"https://raw.githubusercontent.com/tdwg/camtrap-dp/{version}/media-table-schema.json",
        "observations": f"https://raw.githubusercontent.com/tdwg/camtrap-dp/{version}/observations-table-schema.json",
        "event-observations": f"https://raw.githubusercontent.com/tdwg/camtrap-dp/{version}/event-observations-table-schema.json"
    }

    schema_url = schema_urls.get(schema_name)
    print(schema_url)
    if schema_url:
        with urlopen(schema_url) as response:
            data_json = json.loads(response.read().decode())
            return data_json
    else:
        return None


def read_schema_field_names(schema_name, version):
    data_json = read_schema(schema_name, version)

    field_names = []
    for fields in data_json['fields']:
        field_names.append(fields['name'])
    print(field_names)
    return field_names
    
def create_deployments(path, version):
    cols = read_schema_field_names('deployments', version)
    filepath = find_resource(path, 'metadata')
    with Resource(filepath) as metadata:
        # pprint(metadata.read_rows())
        print(metadata.schema)

        df_metadata = metadata.to_pandas()
        df_deployments = pd.DataFrame(columns=cols)
        df_deployments['deploymentID'] = df_metadata['Sample'].astype(str)
        df_deployments['locationID'] = df_metadata['Site']
        df_deployments['locationName'] = df_metadata['Location']
        df_deployments['latitude'] = df_metadata['Latitude']
        df_deployments['longitude'] = df_metadata['Longitude']
        df_deployments['coordinateUncertainty'] = 50
        df_deployments['cameraModel'] = 'Canon Legria HFG25'
        df_deployments['baitUse'] = 'true'
        df_deployments['habitat'] = 'Cover of benthos and score of complexity'
        df_deployments['deploymentStart'] = pd.to_datetime(
            df_metadata['Date'].astype(str)+ df_metadata['Time'].astype(str), 
            format='%Y%m%d%H:%M:%S').apply(lambda x: x.strftime('%Y-%m-%dT%H:%M:%SZ'))
        df_deployments['deploymentEnd'] = pd.to_datetime(
            df_metadata['Date'].astype(str)+ df_metadata['Time'].astype(str), 
            format='%Y%m%d%H:%M:%S').apply(lambda x: x.strftime('%Y-%m-%dT%H:%M:%SZ'))

        deployments = Resource(df_deployments)
        target = deployments.write('output/dp/deployments.csv')

        # Print resulting schema and data
        print(target.schema)
        print(target.to_view())



# mediaID	deploymentID	eventID	captureMethod	timestamp	filePath	filePublic	fileName	fileMediatype	exifData	favorite	mediaComments
# OpCode	Camera	MovieSeqIndex	StartTimeOffset	Format	Filename	    Frames	Rate
# 1.01	    0	    0	            0.00000	        0	    1.01_L373.avi	123778	25.00000
# 1.01	    0	    0	            0.00000	        0	    1.01_R374.avi	123756	25.00000
# 1.01	    1	    0	            0.00000	        0	    1.01_R374.avi	123756	25.00000
# 1.02	    0	    0	            0.00000	        0	    1.02_L369.avi	126299	25.00000
# 1.02	    1	    0	            0.00000	        0	    1.02_R370.avi	126586	25.00000
# 1.03	    0	    0	            0.00000	        0	    1.03_L367.avi	128964	25.00000
# 1.03	    1	    0	            0.00000	        0	    1.03_R368.avi	128255	25.00000
# 1.04	    0	    0	            0.00000	        0	    1.04_L375.avi	133066	25.00000

def create_media(path, version):
    cols = read_schema_field_names('media', version)
    print(cols)
    
    df_metadata = Resource(find_resource(path, 'metadata')).to_pandas()
    time_dict = dict(zip(df_metadata.Sample, pd.to_datetime(
        df_metadata['Date'].astype(str)+ df_metadata['Time'].astype(str), 
        format='%Y%m%d%H:%M:%S').apply(lambda x: x.strftime('%Y-%m-%dT%H:%M:%SZ'))))
    
    filepath = find_resource(path, 'movieseq')
    with open(filepath) as movieseq:
        df_movieseq = pd.read_table(movieseq)
        print(df_movieseq.columns)
        # sample_id = df_movieseq['Filename'].map(lambda x: str(x)[:-9]).drop_duplicates(keep='last')
        # print("xxx============================")
        # print(sample_id)
        # row = df_metadata.loc[df_metadata['Sample'] == sample_id]
        # row = df_metadata[df_metadata.Sample == sample_id]
        # print(row)
        
        # df = pd.DataFrame({'col2': {0: 'a', 1: 1, 2: 2, 3: 3}, 'col1': {0: 'w', 1: 1.01, 2: 2.02, 3: 2.02}})
        # di = {1: "A", 2: "B"}
        # print(df)
        # # df.replace({"col1": di})
        # df["col1"].replace(time_dict, inplace=True)
        # print(df)

        df_media = pd.DataFrame(columns=cols)
        df_media['mediaID'] = df_movieseq['Filename'].map(lambda x: str(x)[:-4]).astype(str)
        df_media['deploymentID'] = df_movieseq['OpCode'].astype(str)
        df_media['captureMethod'] = 'motionDetection'
        df_media['timestamp'] = df_movieseq['Filename'].map(lambda x: str(x)[:-9]).astype('float')
        df_media['filePath'] = 'https://data.csiro.au/collection/'
        df_media['filePublic'] = True
        df_media['fileName'] = df_movieseq['Filename']
        df_media['fileMediatype'] = 'video/x-msvideo'
        df_media['exifData'] = ''
        df_media['favorite'] = ''
        df_media['mediaComments'] = ''
        
        df_media["timestamp"].replace(time_dict, inplace=True)
        df_media = df_media.drop_duplicates(keep='last')

        media = Resource(df_media)
        target = media.write('output/dp/media.csv')

        # Print resulting schema and data
        print(target.schema)
        print(target.to_view())
        
# OpCode	PointIndex  Filename	    Frame	Time	   Period	PeriodTime	ImageCol	ImageRow	Family	        Genus	    Species	        Code	    Number	    Stage	Activity	Comment	Attribute9	Attribute10
# 1.01	    0	        1.01_L373.avi	13293	8.862	    1	    0.018	    1257.16684	985.29851	Labridae	    Coris	    caudimacula	    37384092	1	        AD	    Passing			
# 1.01	    1	        1.01_L373.avi	16267	10.84467	1	    2.00067	    861.17647	784.70588	Pinguipedidae	Parapercis	nebulosa	    37390005	1	        AD	    Passing			
# 1.01	    2	        1.01_L373.avi	16267	10.84467	1	    2.00067	    843.52941	744.70588	Nemipteridae	Pentapodus	nagasakiensis	37347012	1	        AD	    Passing			
# 1.01	    3	        1.01_L373.avi	16267	10.84467	1	    2.00067	    691.76471	700	        Nemipteridae	Pentapodus	nagasakiensis	37347012	1	        AD	    Passing			


def get_date_from_deployment():
    deployments = Resource('output/dp/deployments.csv')
    deployments_dict = deployments.extract()
    name_list = []
    for json_data in deployments_dict:
        data_dict = json_data.to_dict()
        name = data_dict['deploymentStart']
        name_list.append(name)
    # pprint(name_list)
    
    
def fix_date(dt, delta):
    return pd.to_datetime(dt, 
            format='%Y-%m-%dT%H:%M:%SZ') + pd.Timedelta(minutes=float(delta))
    
def create_observations(path, version):
    cols = read_schema_field_names('observations', version)
    filepath = find_resource(path, 'points')
    # print(filepath)
    with open(filepath) as points:
        df_points = pd.read_table(points)
        df_deployments = Resource(find_resource(path, 'metadata')).to_pandas()
        df_points = pd.merge(df_points, df_deployments, left_on='OpCode', right_on='Sample', suffixes=(None, "_dep", ))
        df_points['dateTime'] = pd.to_datetime(df_points['Date'].astype(str)+ df_points['Time_dep'].astype(str), format='%Y%m%d%H:%M:%S').apply(lambda x: x.strftime('%Y-%m-%dT%H:%M:%SZ'))
        df_points['eventStart'] = df_points.apply(lambda row: fix_date(row['dateTime'], row['Time']), axis=1)
        df_points['eventEnd'] = df_points.apply(lambda row: fix_date(row['dateTime'], row['Time']+ row['PeriodTime']), axis=1)
        
        df_observation = pd.DataFrame(columns=cols)
        df_observation['observationID'] = df_points['Filename'].map(lambda x: str(x)[:-9]) + "-" + "points-" + df_points['PointIndex'].astype(str)  
        df_observation['deploymentID'] = df_points['OpCode'].astype(str)
        df_observation['eventID'] = "e_" + df_points['OpCode'].astype(str)
        df_observation['eventStart'] = df_points['eventStart']
        df_observation['eventEnd'] = df_points['eventEnd']
        df_observation['observationLevel'] = "media"
        df_observation['mediaID'] = df_points['Filename'].map(lambda x: str(x)[:-4])
        df_observation['observationType'] = 'animal'
        df_observation['cameraSetupType'] = ''
        df_observation['taxonID'] = df_points['Code']
        df_observation['scientificName'] = df_points['Species']
        df_observation['count'] = df_points['Number']
        df_observation['lifeStage'] = df_points['Stage'].map({'AD': 'adult'})
        df_observation['sex'] = ''
        df_observation['behavior'] = ''
        df_observation['individualID'] = "ind_" + df_points['PointIndex'].astype(str) + "_" + df_points['Filename'].map(lambda x: str(x)[:-4])
        df_observation['individualPositionRadius'] = ''
        df_observation['individualPositionAngle'] = ''
        df_observation['classificationMethod'] = 'human'
        df_observation['classifiedBy'] = ''
        df_observation['classificationTimestamp'] = ''
        df_observation['classificationProbability'] = ''
        df_observation['observationTags'] = ''
        df_observation['observationComments'] = ''

        media = Resource(df_observation)
        target = media.write('output/dp/observations.csv')

        # Print resulting schema and data
        print(target.schema)
        print(target.to_view())
        
def create_datapackage(path, version):
    profile = f"https://raw.githubusercontent.com/tdwg/camtrap-dp/{version}/camtrap-dp-profile.json"
    response = urlopen(profile)
    data_json = json.loads(response.read())
    # print(data_json)

    filepath = find_resource(path, 'points')
    # print(filepath)

    with open('output/dp/datapackage.json') as json_file:
        data_json = json.load(json_file)
        taxonomic = data_json.get("taxonomic")
        taxonomic_code = [taxon.get("taxonID") for taxon in taxonomic]

        with open(filepath) as points:
            df_points = pd.read_table(points)
            for point in df_points.itertuples():
                code = int(point.Code) if not math.isnan(point.Code) else None
                if code and code not in taxonomic_code:
                    taxonomic_ins = {
                        "family": point.Family,
                        "genus": point.Genus,
                        "species": point.Species,
                        "scientificName": f"{point.Genus} {point.Species}",
                        "taxonRank": "species",
                        "taxonID": code,
                        "taxonIDReference": f"https://www.marine.csiro.au/data/caab/taxon_report.cfm?caab_code={code}"
                    }
                    taxonomic.append(taxonomic_ins)
                    taxonomic_code.append(code)
            
        with open('output/dp/datapackage.json', 'w') as fp:
            json.dump(data_json, fp, indent=4)
            
            report = validate('output/dp/datapackage.json')
            print(report)
            # package = Package('output/dp/datapackage.json')
            # pprint(package.extract())

def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")
    
    schema = subparser.add_parser("schema")
    datapackage = subparser.add_parser("datapackage")
    deployments = subparser.add_parser("deployments")
    media = subparser.add_parser("media")
    observations = subparser.add_parser("observations")
    all = subparser.add_parser("all")
    
    schema.add_argument("-s", "--schema", type=str, required=True)
    schema.add_argument("-v", "--version", type=str, required=True)
    datapackage.add_argument("-p", "--path", type=str, required=True)
    datapackage.add_argument("-v", "--version", type=str, required=True)
    deployments.add_argument("-p", "--path", type=str, required=True)
    deployments.add_argument("-v", "--version", type=str, required=True)
    media.add_argument("-p", "--path", type=str, required=True)
    media.add_argument("-v", "--version", type=str, required=True)
    observations.add_argument("-p", "--path", type=str, required=True)
    observations.add_argument("-v", "--version", type=str, required=True)
    all.add_argument("-p", "--path", type=str, required=True)
    all.add_argument("-v", "--version", type=str, required=True)
    
    args = parser.parse_args()
    if args.command == "schema":
        read_schema(args.schema, args.version)
    if args.command == "datapackage":
        create_datapackage(args.path, args.version)
    elif args.command == "deployments":
        create_deployments(args.path, args.version)
    elif args.command == "media":
        create_media(args.path, args.version)
    elif args.command == "observations":
        create_observations(args.path, args.version)
    elif args.command == "all":
        create_deployments(args.path, args.version)
        create_media(args.path, args.version)
        create_observations(args.path, args.version)
if __name__ == "__main__":
    main()