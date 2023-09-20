from sqlalchemy.orm import Session

import csv
import models
import database
import pandas as pd
from pprint import pprint
from frictionless import Package
from frictionless import Resource, Detector
from sqlalchemy.orm import make_transient


def get_agent(db_session: Session):
    with database.SessionLocal() as db_session:
        return (
            db_session.query(models.Agent).all()
        )
    
def get_location(deployment_id: str):
    with database.SessionLocal() as db_session:
        return (
            db_session.query(models.Location)
            .filter(models.Location.location_id == str(deployment_id)) \
            .first()
        )

def get_event(media_id: str):
    with database.SessionLocal() as db_session:
        return (
            db_session.query(models.Event)
            .filter(models.Event.event_id == str(media_id)) \
            .first()
        )


def add_agent(
    agent_id: str,
    agent_type: str,
    preferred_agent_name: str
):
    agent = models.Agent(
        agent_id = agent_id,
        agent_type = agent_type,
        preferred_agent_name = preferred_agent_name
    )
    add_to_db(agent)
    return agent


def add_georeference(resource: dict):
    georeference = models.Georeference(
        georeference_id = resource.get('deploymentID'),
        location_id = resource.get('deploymentID'),
        decimal_latitude = resource.get('latitude'),
        decimal_longitude = resource.get('longitude'),
        geodetic_datum = '',
        coordinate_uncertainty_in_meters = resource.get('coordinateUncertainty'),
        coordinate_precision = None,
        point_radius_spatial_fit = None,
        footprint_wkt = None,
        footprint_srs = None,
        footprint_spatial_fit = None,
        georeferenced_by = None,
        georeferenced_date = None,
        georeference_protocol = None,
        georeference_sources = None,
        georeference_remarks = None,
        preferred_spatial_representation = None,
    )
    return add_to_db(georeference)


def add_location(resource: dict):
    location = models.Location(
        location_id = resource.get('deploymentID'),
        parent_location_id = None,
        higher_geography_id = None,
        higher_geography = None,
        continent = None,
        water_body = None,
        island_group = None,
        island = None,
        country = None,
        country_code = None,
        state_province = None,
        county = None,
        municipality = None,
        locality = resource.get('locationName'),
        minimum_elevation_in_meters = None,
        maximum_elevation_in_meters = None,
        minimum_distance_above_surface_in_meters = None,
        maximum_distance_above_surface_in_meters = None,
        minimum_depth_in_meters = None,
        maximum_depth_in_meters = None,
        vertical_datum = None,
        location_according_to = None,
        location_remarks = None,
        accepted_georeference_id = None,
        accepted_geological_context_id = None,
    )
    add_to_db(location)
    return location
            

def add_event_deployments(resource: dict):
    location = get_location(resource.get('deploymentID'))
    event = models.Event(
        event_id = resource.get('deploymentID'),
        parent_event_id = None,
        dataset_id = 'ningaloo',
        location_id = location.location_id,
        protocol_id = None,
        event_type = 'deployment',
        event_name = None,
        field_number = None,
        event_date = resource.get('start'),
        year = None,
        month = None,
        day = None,
        verbatim_event_date = None,
        verbatim_locality = None,
        verbatim_elevation = None,
        verbatim_depth = None,
        verbatim_coordinates = None,
        verbatim_latitude = None,
        verbatim_longitude = None,
        verbatim_coordinate_system = None,
        verbatim_srs = None,
        habitat = resource.get('habitat'),
        protocol_description = None,
        sample_size_value = None,
        sample_size_unit = None,
        event_effort = None,
        field_notes = None,
        event_remarks = resource.get('deploymentComments'),
    )
    return add_to_db(event)

def add_event_media(resource: dict):
    location = get_location(resource.get('deploymentID'))
    event = models.Event(
        event_id = resource.get('mediaID'),
        parent_event_id = resource.get('deploymentID'),
        dataset_id = 'ningaloo',
        location_id = location.location_id,
        protocol_id = None,
        event_type = 'image capture',
        event_name = None,
        field_number = None,
        event_date = resource.get('start'),
        year = None,
        month = None,
        day = None,
        verbatim_event_date = None,
        verbatim_locality = None,
        verbatim_elevation = None,
        verbatim_depth = None,
        verbatim_coordinates = None,
        verbatim_latitude = None,
        verbatim_longitude = None,
        verbatim_coordinate_system = None,
        verbatim_srs = None,
        habitat = resource.get('habitat'),
        protocol_description = None,
        sample_size_value = None,
        sample_size_unit = None,
        event_effort = None,
        field_notes = None,
        event_remarks = resource.get('deploymentComments'),
    )
    return add_to_db(event)

def add_event_media_observation(resource: dict):
    event = get_event(resource.get('mediaID'))
    event = models.Event(
        event_id = resource.get('observationID'),
        parent_event_id = resource.get('mediaID'),
        dataset_id = 'ningaloo',
        location_id = event.location_id,
        protocol_id = None,
        event_type = 'observation',
        event_name = None,
        field_number = None,
        event_date = resource.get('start'),
        year = None,
        month = None,
        day = None,
        verbatim_event_date = None,
        verbatim_locality = None,
        verbatim_elevation = None,
        verbatim_depth = None,
        verbatim_coordinates = None,
        verbatim_latitude = None,
        verbatim_longitude = None,
        verbatim_coordinate_system = None,
        verbatim_srs = None,
        habitat = resource.get('habitat'),
        protocol_description = None,
        sample_size_value = None,
        sample_size_unit = None,
        event_effort = None,
        field_notes = None,
        event_remarks = resource.get('deploymentComments'),
    )
    return add_to_db(event)


def add_digital_entity(resource: dict):
    digital_entity = models.DigitalEntity(
        digital_entity_id = f"digent_{resource.get('mediaID')}",
        digital_entity_type = 'MOVING_IMAGE',
        access_uri = resource.get('filePath'),
        web_statement = None,
        format = resource.get('fileMediatype'),
        license = None,
        rights = None,
        rights_uri = None,
        access_rights = None,
        rights_holder = None,
        source = None,
        source_uri = None,
        creator = None,
        created = resource.get('timestamp'),
        modified = None,
        language = None,
        bibliographic_citation = None,
        entity_id = f"digent_{resource.get('mediaID')}",
        entity_type = 'DIGITAL_ENTITY',
        dataset_id = 'ningaloo',
        entity_name = resource.get('fileName'),
        entity_remarks = resource.get('mediaComments')
    )
    return add_to_db(digital_entity)

def add_organism(resource: dict):
    entity = models.Organism(
        organism_id = f"org_{resource.get('observationID')}",
        organism_scope = 'individual',
        accepted_identification_id = None,
        
        material_entity_id = f"org_{resource.get('observationID')}",
        material_entity_type = 'Organism',
        preparations = None,
        disposition = None,
        institution_code = None,
        institution_id = None,
        collection_code = None,
        collection_id = None,
        owner_institution_code = None,
        catalog_number = None,
        record_number = None,
        recorded_by = None,
        recorded_by_id = None,
        associated_references = None,
        associated_sequences = None,
        other_catalog_numbers = None,
        entity_id = f"org_{resource.get('observationID')}",
        entity_type = 'MATERIAL_ENTITY',
        dataset_id = 'ningaloo',
        entity_name = None,
        entity_remarks = None
    )
    return add_to_db(entity)

def add_identification(resource: dict):
    entity = models.Identification(
        
        identification_id = resource.get('individualID'),
        organism_id = f"org_{resource.get('observationID')}",
        identification_type = resource.get('classificationMethod'),
        taxon_formula = resource.get('taxonID'),
        verbatim_identification = resource.get('scientificName'),
        type_status = None,
        identified_by = resource.get('classifiedBy'),
        identified_by_id = resource.get('classifiedBy'),
        date_identified = resource.get('classificationTimestamp'),
        identification_references = None,
        identification_verification_status = None,
        identification_remarks = None,
        type_designation_type = None,
        type_designated_by = None
    )
    return add_to_db(entity)


def add_taxon(resource: dict):
    entity = models.Taxon(
        
        taxon_id = resource.get('taxonID'),
        scientific_name = resource.get('scientificName'),
        scientific_name_authorship = None,
        name_according_to = None,
        name_according_to_id = None,
        taxon_rank = None,
        taxon_source = None,
        scientific_name_id = None,
        taxon_remarks = None,
        parent_taxon_id = None,
        taxonomic_status = None,
        kingdom = None,
        phylum = None,
        _class = None,
        order = None,
        family = None,
        subfamily = None,
        genus = None,
        subgenus = None,
        accepted_scientific_name =None
    )
    return add_to_db(entity)
    

def add_taxon_identification(resource: dict):
    entity = models.TaxonIdentification(
        taxon_id = resource.get('taxonID'),
        identification_id = resource.get('individualID'),
        taxon_order = None,
        taxon_authority = None
    )
    return add_to_db(entity)

def add_assertions_lifestage(resource: dict):
    entity = models.Assertion(
        assertion_id = f"assert_lifeStage_{resource.get('observationID')}",
        assertion_target_id = f"org_{resource.get('observationID')}",
        assertion_target_type = 'ORGANISM', #Column(Enum('ENTITY', 'MATERIAL_ENTITY', 'MATERIAL_GROUP', 'ORGANISM', 'DIGITAL_ENTITY', 'GENETIC_SEQUENCE', 'EVENT', 'OCCURRENCE', 'LOCATION', 'GEOREFERENCE', 'GEOLOGICAL_CONTEXT', 'PROTOCOL', 'AGENT', 'COLLECTION', 'ENTITY_RELATIONSHIP', 'IDENTIFICATION', 'TAXON', 'REFERENCE', 'AGENT_GROUP', 'ASSERTION', 'CHRONOMETRIC_AGE', name='common_targets'), nullable=False, index=True)
        assertion_parent_assertion_id = None,
        assertion_type = 'lifeStage',
        assertion_made_date = resource.get('classificationTimestamp'),
        assertion_effective_date = None,
        assertion_value = resource.get('lifeStage'),
        assertion_value_numeric = None,
        assertion_unit = None, 
        assertion_by_agent_name = None, 
        assertion_by_agent_id = None, 
        assertion_protocol = None, 
        assertion_protocol_id = None, 
        assertion_remarks = None
    )
    return add_to_db(entity)

def add_assertions_count(resource: dict):
    entity = models.Assertion(
        assertion_id = f"assert_count_{resource.get('observationID')}",
        assertion_target_id = f"org_{resource.get('observationID')}",
        assertion_target_type = 'ORGANISM', #Column(Enum('ENTITY', 'MATERIAL_ENTITY', 'MATERIAL_GROUP', 'ORGANISM', 'DIGITAL_ENTITY', 'GENETIC_SEQUENCE', 'EVENT', 'OCCURRENCE', 'LOCATION', 'GEOREFERENCE', 'GEOLOGICAL_CONTEXT', 'PROTOCOL', 'AGENT', 'COLLECTION', 'ENTITY_RELATIONSHIP', 'IDENTIFICATION', 'TAXON', 'REFERENCE', 'AGENT_GROUP', 'ASSERTION', 'CHRONOMETRIC_AGE', name='common_targets'), nullable=False, index=True)
        assertion_parent_assertion_id = None,
        assertion_type = 'organismQuantity',
        assertion_made_date = resource.get('classificationTimestamp'),
        assertion_effective_date = None,
        assertion_value = None,
        assertion_value_numeric = resource.get('count'),
        assertion_unit = 'individual', 
        assertion_by_agent_name = None, 
        assertion_by_agent_id = None, 
        assertion_protocol = None, 
        assertion_protocol_id = None, 
        assertion_remarks = None
    )
    return add_to_db(entity)

def manage_location(package):
    with package.get_resource('deployments') as resource:
        for row in resource.row_stream:   
            deployment = row.to_dict(json=False)
            add_location(resource=deployment)
            add_georeference(resource=deployment)

def manage_event(package):
    # deployments = package.get_resource('deployments')
    # pprint(deployments.read_rows())
    # print(type(deployments))
    # pprint(deployments.header)
    with package.get_resource('deployments') as resource:
        for row in resource.row_stream:   
            # print(f'Row: {row}')
            deployment = row.to_dict(json=False)
            event_deployment = add_event_deployments(resource=deployment)
            print(f"event_deployment: {event_deployment}")
                       
    # media = package.get_resource('media')
    # pprint(media.read_rows())
    # pprint(media.header)
    with package.get_resource('media') as resource:
        for row in resource.row_stream:   
            media_dict = row.to_dict(json=False)
            event_media = add_event_media(resource=media_dict)
            print(f"event_media: {event_media}")
            
    # media_observation = package.get_resource('media-observations')
    # pprint(media_observation.read_rows())
    # pprint(media_observation.header)
    with package.get_resource('media-observations') as resource:
        for row in resource.row_stream:   
            media_observation_dict = row.to_dict(json=False)
            event_media_observation = add_event_media_observation(resource=media_observation_dict)
            print(f"event_media_observation: {event_media_observation}")
             
def manage_taxon_identification(package):
    with package.get_resource('media-observations') as resource:
        for row in resource.row_stream:   
            media_observation_dict = row.to_dict(json=False)
            with database.SessionLocal() as db_session:
                exists = db_session.query(models.Taxon).filter(models.Taxon.taxon_id == str(media_observation_dict.get('taxonID'))).first() is not None
                if not exists:
                    taxon = add_taxon(resource=media_observation_dict)
                    print(f"taxon: {taxon}")
                
                    taxon_identification = add_taxon_identification(resource=media_observation_dict)
                    print(f"taxon_identification: {taxon_identification}")
                
            
def manage_assertion(package):
    with package.get_resource('media-observations') as resource:
        for row in resource.row_stream:   
            media_observation_dict = row.to_dict(json=False)
            
            assertions_count = add_assertions_count(resource=media_observation_dict)
            print(f"assertions_count: {assertions_count}")
            
            assertions_lifestage = add_assertions_lifestage(resource=media_observation_dict)
            print(f"assertions_lifestage: {assertions_lifestage}")

def manage_entity(package):
    with package.get_resource('media') as resource:
        for row in resource.row_stream:   
            media_dict = row.to_dict(json=False)
            digital_entity_media = add_digital_entity(resource=media_dict)
            print(f"digital_entity_media: {digital_entity_media}")
        print("End add digital entitty\n\n\n\n")
    
    with package.get_resource('media-observations') as resource:
        for row in resource.row_stream:   
            media_observation_dict = row.to_dict(json=False)
            
            organism_media_observation = add_organism(resource=media_observation_dict)
            print(f"organism_media_observation: {organism_media_observation}")
            
            
            identification_media_observation = add_identification(resource=media_observation_dict)
            print(f"identification_media_observation: {identification_media_observation}")
            
def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        column_name = "_class" if column.name == 'class' else column.name
        val = getattr(row, column_name)
        if val is not None:
            d[column.name] = val
    return d


def add_to_db(entity):
    with database.SessionLocal() as db_session:
        entity_dict = row2dict(entity)
        print(entity_dict)
        db_session.add(entity)
        db_session.commit()
        # make_transient(entity)
        # db_session.expunge_all()
        # db_session.close()
        return entity_dict
   
   
def manage_export():
    entity_list = [models.Location, models.Georeference, models.Event, models.Entity, models.DigitalEntity, models.MaterialEntity, models.Organism, models.Assertion, models.Identification, models.Taxon, models.TaxonIdentification]
    for entity in entity_list:
        export_to_csv(entity)
    
def export_to_csv(entity):
    with database.SessionLocal() as db_session:
        with open(f"output/gum/{entity.__table__.name}.csv", 'w') as outfile:
            outcsv = csv.writer(outfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)
            records = db_session.query(entity).all()
            header = entity.__table__.columns.keys()
            print(header)
            outcsv.writerow(header)
            for record in records:
                outcsv.writerow([getattr(record, "_class" if c == 'class' else c) for c in header ])


def main():
    # package = Package('output/datapackage.json')
    package = Package('output/dp/*.csv')
    # pprint(package.extract())

    database.truncate_db()
    manage_location(package)
    manage_event(package)
    manage_entity(package)
    manage_assertion(package)
    manage_taxon_identification(package)
    
    manage_export()
    
    
        
if __name__ == "__main__":
    main()
