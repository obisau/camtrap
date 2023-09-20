from sqlalchemy import Boolean, CHAR, CheckConstraint, Column, DateTime, Enum, ForeignKey, Index, Integer, Numeric, SmallInteger, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base

metadata = Base.metadata

class Agent(Base):
    __tablename__ = 'agent'

    agent_id = Column(Text, primary_key=True)
    agent_type = Column(Text, nullable=False)
    preferred_agent_name = Column(Text)


class AgentGroup(Agent):
    __tablename__ = 'agent_group'

    agent_group_id = Column(ForeignKey('agent.agent_id', ondelete='CASCADE', deferrable=True), primary_key=True)
    agent_group_type = Column(Text)


class Collection(Agent):
    __tablename__ = 'collection'

    collection_id = Column(ForeignKey('agent.agent_id', ondelete='CASCADE', deferrable=True), primary_key=True)
    collection_type = Column(Text)
    collection_code = Column(Text)
    institution_code = Column(Text)
    grscicoll_id = Column(UUID)


class Entity(Base):
    __tablename__ = 'entity'

    entity_id = Column(Text, primary_key=True)
    entity_type = Column(Enum('DIGITAL_ENTITY', 'MATERIAL_ENTITY', name='entity_type'), nullable=False, index=True)
    dataset_id = Column(Text, nullable=False)
    entity_name = Column(Text)
    entity_remarks = Column(Text)

    occurrences = relationship('Occurrence', secondary='occurrence_evidence')
    identifications = relationship('Identification', secondary='identification_evidence')


class DigitalEntity(Entity):
    __tablename__ = 'digital_entity'

    digital_entity_id = Column(Text, ForeignKey('entity.entity_id', ondelete='CASCADE', deferrable=True), primary_key=True)
    digital_entity_type = Column(Enum('DATASET', 'INTERACTIVE_RESOURCE', 'MOVING_IMAGE', 'SERVICE', 'SOFTWARE', 'SOUND', 'STILL_IMAGE', 'TEXT', 'GENETIC_SEQUENCE', name='digital_entity_type'), nullable=False, index=True)
    access_uri = Column(Text, nullable=False)
    web_statement = Column(Text)
    format = Column(Text)
    license = Column(Text)
    rights = Column(Text)
    rights_uri = Column(Text)
    access_rights = Column(Text)
    rights_holder = Column(Text)
    source = Column(Text)
    source_uri = Column(Text)
    creator = Column(Text)
    created = Column(DateTime(True))
    modified = Column(DateTime(True))
    language = Column(Text)
    bibliographic_citation = Column(Text)
    

class GeneticSequence(DigitalEntity):
    __tablename__ = 'genetic_sequence'

    genetic_sequence_id = Column(ForeignKey('digital_entity.digital_entity_id', ondelete='CASCADE', deferrable=True), primary_key=True)
    genetic_sequence_type = Column(Text, nullable=False)
    sequence = Column(Text, nullable=False)


class MaterialEntity(Entity):
    __tablename__ = 'material_entity'

    material_entity_id = Column(ForeignKey('entity.entity_id', ondelete='CASCADE', deferrable=True), primary_key=True)
    material_entity_type = Column(Text, nullable=False)
    preparations = Column(Text)
    disposition = Column(Text)
    institution_code = Column(Text)
    institution_id = Column(Text)
    collection_code = Column(Text)
    collection_id = Column(ForeignKey('collection.collection_id', ondelete='CASCADE', deferrable=True))
    owner_institution_code = Column(Text)
    catalog_number = Column(Text)
    record_number = Column(Text)
    recorded_by = Column(Text)
    recorded_by_id = Column(Text)
    associated_references = Column(Text)
    associated_sequences = Column(Text)
    other_catalog_numbers = Column(Text)

    collection = relationship('Collection')


class Organism(MaterialEntity):
    __tablename__ = 'organism'

    organism_id = Column(ForeignKey('material_entity.material_entity_id', ondelete='CASCADE', deferrable=True), primary_key=True)
    organism_scope = Column(Text)
    accepted_identification_id = Column(ForeignKey('identification.identification_id', ondelete='SET NULL', deferrable=True))

    accepted_identification = relationship('Identification', primaryjoin='Organism.accepted_identification_id == Identification.identification_id')


class MaterialGroup(MaterialEntity):
    __tablename__ = 'material_group'

    material_group_id = Column(ForeignKey('material_entity.material_entity_id', ondelete='CASCADE', deferrable=True), primary_key=True)
    material_group_type = Column(Text)


class GeologicalContext(Base):
    __tablename__ = 'geological_context'

    geological_context_id = Column(Text, primary_key=True)
    location_id = Column(ForeignKey('location.location_id', ondelete='CASCADE', deferrable=True), index=True)
    earliest_eon_or_lowest_eonothem = Column(Text)
    latest_eon_or_highest_eonothem = Column(Text)
    earliest_era_or_lowest_erathem = Column(Text)
    latest_era_or_highest_erathem = Column(Text)
    earliest_period_or_lowest_system = Column(Text)
    latest_period_or_highest_system = Column(Text)
    earliest_epoch_or_lowest_series = Column(Text)
    latest_epoch_or_highest_series = Column(Text)
    earliest_age_or_lowest_stage = Column(Text)
    latest_age_or_highest_stage = Column(Text)
    lowest_biostratigraphic_zone = Column(Text)
    highest_biostratigraphic_zone = Column(Text)
    lithostratigraphic_terms = Column(Text)
    group = Column(Text)
    formation = Column(Text)
    member = Column(Text)
    bed = Column(Text)

    location = relationship('Location', primaryjoin='GeologicalContext.location_id == Location.location_id')


class Georeference(Base):
    __tablename__ = 'georeference'
    __table_args__ = (
        CheckConstraint('(coordinate_precision >= (0)::numeric) AND (coordinate_precision <= (90)::numeric)'),
        CheckConstraint('(coordinate_uncertainty_in_meters > (0)::numeric) AND (coordinate_uncertainty_in_meters <= (20037509)::numeric)'),
        CheckConstraint("(decimal_latitude >= ('-90'::integer)::numeric) AND (decimal_latitude <= (90)::numeric)"),
        CheckConstraint("(decimal_longitude >= ('-180'::integer)::numeric) AND (decimal_longitude <= (180)::numeric)"),
        CheckConstraint('(point_radius_spatial_fit = (0)::numeric) OR (point_radius_spatial_fit >= (1)::numeric)'),
        CheckConstraint('footprint_spatial_fit >= (0)::numeric')
    )

    georeference_id = Column(Text, primary_key=True)
    location_id = Column(ForeignKey('location.location_id', ondelete='CASCADE', deferrable=True), index=True)
    decimal_latitude = Column(Numeric, nullable=False)
    decimal_longitude = Column(Numeric, nullable=False)
    geodetic_datum = Column(Text, nullable=False)
    coordinate_uncertainty_in_meters = Column(Numeric)
    coordinate_precision = Column(Numeric)
    point_radius_spatial_fit = Column(Numeric)
    footprint_wkt = Column(Text)
    footprint_srs = Column(Text)
    footprint_spatial_fit = Column(Numeric)
    georeferenced_by = Column(Text)
    georeferenced_date = Column(Text)
    georeference_protocol = Column(Text)
    georeference_sources = Column(Text)
    georeference_remarks = Column(Text)
    preferred_spatial_representation = Column(Text)

    location = relationship('Location', primaryjoin='Georeference.location_id == Location.location_id')


class Identification(Base):
    __tablename__ = 'identification'

    identification_id = Column(Text, primary_key=True)
    organism_id = Column(ForeignKey('organism.organism_id', ondelete='CASCADE', deferrable=True))
    identification_type = Column(Text, nullable=False)
    taxon_formula = Column(Text, nullable=False)
    verbatim_identification = Column(Text)
    type_status = Column(Text)
    identified_by = Column(Text)
    identified_by_id = Column(Text)
    date_identified = Column(Text)
    identification_references = Column(Text)
    identification_verification_status = Column(Text)
    identification_remarks = Column(Text)
    type_designation_type = Column(Text)
    type_designated_by = Column(Text)

    organism = relationship('Organism', primaryjoin='Identification.organism_id == Organism.organism_id')


class Identifier(Base):
    __tablename__ = 'identifier'

    identifier_target_id = Column(Text, primary_key=True, nullable=False)
    identifier_target_type = Column(Enum('ENTITY', 'MATERIAL_ENTITY', 'MATERIAL_GROUP', 'ORGANISM', 'DIGITAL_ENTITY', 'GENETIC_SEQUENCE', 'EVENT', 'OCCURRENCE', 'LOCATION', 'GEOREFERENCE', 'GEOLOGICAL_CONTEXT', 'PROTOCOL', 'AGENT', 'COLLECTION', 'ENTITY_RELATIONSHIP', 'IDENTIFICATION', 'TAXON', 'REFERENCE', 'AGENT_GROUP', 'ASSERTION', 'CHRONOMETRIC_AGE', name='common_targets'), primary_key=True, nullable=False, index=True)
    identifier_type = Column(Text, primary_key=True, nullable=False)
    identifier_value = Column(Text, primary_key=True, nullable=False)


class Location(Base):
    __tablename__ = 'location'
    __table_args__ = (
        CheckConstraint('(maximum_depth_in_meters >= (0)::numeric) AND (maximum_depth_in_meters <= (11000)::numeric)'),
        CheckConstraint("(maximum_elevation_in_meters >= ('-430'::integer)::numeric) AND (maximum_elevation_in_meters <= (8850)::numeric)"),
        CheckConstraint('(minimum_depth_in_meters >= (0)::numeric) AND (minimum_depth_in_meters <= (11000)::numeric)'),
        CheckConstraint("(minimum_elevation_in_meters >= ('-430'::integer)::numeric) AND (minimum_elevation_in_meters <= (8850)::numeric)")
    )

    location_id = Column(Text, primary_key=True)
    parent_location_id = Column(ForeignKey('location.location_id', ondelete='CASCADE', deferrable=True), index=True)
    higher_geography_id = Column(Text)
    higher_geography = Column(Text)
    continent = Column(Text)
    water_body = Column(Text)
    island_group = Column(Text)
    island = Column(Text)
    country = Column(Text)
    country_code = Column(CHAR(2))
    state_province = Column(Text)
    county = Column(Text)
    municipality = Column(Text)
    locality = Column(Text)
    minimum_elevation_in_meters = Column(Numeric)
    maximum_elevation_in_meters = Column(Numeric)
    minimum_distance_above_surface_in_meters = Column(Numeric)
    maximum_distance_above_surface_in_meters = Column(Numeric)
    minimum_depth_in_meters = Column(Numeric)
    maximum_depth_in_meters = Column(Numeric)
    vertical_datum = Column(Text)
    location_according_to = Column(Text)
    location_remarks = Column(Text)
    accepted_georeference_id = Column(ForeignKey('georeference.georeference_id', ondelete='SET NULL', deferrable=True))
    accepted_geological_context_id = Column(ForeignKey('geological_context.geological_context_id', ondelete='SET NULL', deferrable=True))

    accepted_geological_context = relationship('GeologicalContext', primaryjoin='Location.accepted_geological_context_id == GeologicalContext.geological_context_id')
    accepted_georeference = relationship('Georeference', primaryjoin='Location.accepted_georeference_id == Georeference.georeference_id')
    parent_location = relationship('Location', remote_side=[location_id])


class Protocol(Base):
    __tablename__ = 'protocol'

    protocol_id = Column(Text, primary_key=True)
    protocol_type = Column(Text, nullable=False)


class Reference(Base):
    __tablename__ = 'reference'
    __table_args__ = (
        CheckConstraint('(reference_year >= 1600) AND (reference_year <= 2022)'),
    )

    reference_id = Column(Text, primary_key=True)
    reference_type = Column(Text, nullable=False)
    bibliographic_citation = Column(Text)
    reference_year = Column(SmallInteger)
    reference_iri = Column(Text)
    is_peer_reviewed = Column(Boolean)


class Taxon(Base):
    __tablename__ = 'taxon'

    taxon_id = Column(Text, primary_key=True)
    scientific_name = Column(Text, nullable=False)
    scientific_name_authorship = Column(Text)
    name_according_to = Column(Text)
    name_according_to_id = Column(Text)
    taxon_rank = Column(Text)
    taxon_source = Column(Text)
    scientific_name_id = Column(Text)
    taxon_remarks = Column(Text)
    parent_taxon_id = Column(ForeignKey('taxon.taxon_id', ondelete='CASCADE', deferrable=True), index=True)
    taxonomic_status = Column(Text)
    kingdom = Column(Text)
    phylum = Column(Text)
    _class = Column('class', Text)
    order = Column(Text)
    family = Column(Text)
    subfamily = Column(Text)
    genus = Column(Text)
    subgenus = Column(Text)
    accepted_scientific_name = Column(Text)

    parent_taxon = relationship('Taxon', remote_side=[taxon_id])


class AgentRelationship(Base):
    __tablename__ = 'agent_relationship'

    subject_agent_id = Column(ForeignKey('agent.agent_id', ondelete='CASCADE', deferrable=True), primary_key=True, nullable=False)
    relationship_to = Column(Text, primary_key=True, nullable=False)
    object_agent_id = Column(ForeignKey('agent.agent_id', ondelete='CASCADE', deferrable=True), primary_key=True, nullable=False)

    object_agent = relationship('Agent', primaryjoin='AgentRelationship.object_agent_id == Agent.agent_id')
    subject_agent = relationship('Agent', primaryjoin='AgentRelationship.subject_agent_id == Agent.agent_id')


t_agent_role = Table(
    'agent_role', metadata,
    Column('agent_role_target_id', Text, nullable=False),
    Column('agent_role_target_type', Enum('ENTITY', 'MATERIAL_ENTITY', 'MATERIAL_GROUP', 'ORGANISM', 'DIGITAL_ENTITY', 'GENETIC_SEQUENCE', 'EVENT', 'OCCURRENCE', 'LOCATION', 'GEOREFERENCE', 'GEOLOGICAL_CONTEXT', 'PROTOCOL', 'AGENT', 'COLLECTION', 'ENTITY_RELATIONSHIP', 'IDENTIFICATION', 'TAXON', 'REFERENCE', 'AGENT_GROUP', 'ASSERTION', 'CHRONOMETRIC_AGE', name='common_targets'), nullable=False, index=True),
    Column('agent_role_agent_id', ForeignKey('agent.agent_id', ondelete='CASCADE', deferrable=True)),
    Column('agent_role_agent_name', Text),
    Column('agent_role_role', Text),
    Column('agent_role_began', Text),
    Column('agent_role_ended', Text),
    Column('agent_role_order', SmallInteger, nullable=False, server_default=text("0")),
    CheckConstraint('agent_role_order >= 0'),
    UniqueConstraint('agent_role_target_id', 'agent_role_target_type', 'agent_role_agent_id', 'agent_role_agent_name', 'agent_role_role', 'agent_role_began', 'agent_role_ended', 'agent_role_order')
)


class Assertion(Base):
    __tablename__ = 'assertion'
    __table_args__ = (
        Index('assertion_assertion_target_type_assertion_target_id_idx', 'assertion_target_type', 'assertion_target_id'),
    )

    assertion_id = Column(Text, primary_key=True)
    assertion_target_id = Column(Text, nullable=False)
    assertion_target_type = Column(Enum('ENTITY', 'MATERIAL_ENTITY', 'MATERIAL_GROUP', 'ORGANISM', 'DIGITAL_ENTITY', 'GENETIC_SEQUENCE', 'EVENT', 'OCCURRENCE', 'LOCATION', 'GEOREFERENCE', 'GEOLOGICAL_CONTEXT', 'PROTOCOL', 'AGENT', 'COLLECTION', 'ENTITY_RELATIONSHIP', 'IDENTIFICATION', 'TAXON', 'REFERENCE', 'AGENT_GROUP', 'ASSERTION', 'CHRONOMETRIC_AGE', name='common_targets'), nullable=False, index=True)
    assertion_parent_assertion_id = Column(ForeignKey('assertion.assertion_id', ondelete='CASCADE', deferrable=True))
    assertion_type = Column(Text, nullable=False)
    assertion_made_date = Column(Text)
    assertion_effective_date = Column(Text)
    assertion_value = Column(Text)
    assertion_value_numeric = Column(Numeric)
    assertion_unit = Column(Text)
    assertion_by_agent_name = Column(Text)
    assertion_by_agent_id = Column(ForeignKey('agent.agent_id', ondelete='CASCADE', deferrable=True))
    assertion_protocol = Column(Text)
    assertion_protocol_id = Column(ForeignKey('protocol.protocol_id', ondelete='CASCADE', deferrable=True))
    assertion_remarks = Column(Text)

    assertion_by_agent = relationship('Agent')
    assertion_parent_assertion = relationship('Assertion', remote_side=[assertion_id])
    assertion_protocol1 = relationship('Protocol')


t_citation = Table(
    'citation', metadata,
    Column('citation_target_id', Text, nullable=False),
    Column('citation_target_type', Enum('ENTITY', 'MATERIAL_ENTITY', 'MATERIAL_GROUP', 'ORGANISM', 'DIGITAL_ENTITY', 'GENETIC_SEQUENCE', 'EVENT', 'OCCURRENCE', 'LOCATION', 'GEOREFERENCE', 'GEOLOGICAL_CONTEXT', 'PROTOCOL', 'AGENT', 'COLLECTION', 'ENTITY_RELATIONSHIP', 'IDENTIFICATION', 'TAXON', 'REFERENCE', 'AGENT_GROUP', 'ASSERTION', 'CHRONOMETRIC_AGE', name='common_targets'), nullable=False, index=True),
    Column('citation_reference_id', ForeignKey('reference.reference_id', ondelete='CASCADE', deferrable=True)),
    Column('citation_type', Text),
    Column('citation_page_number', Text),
    Column('citation_remarks', Text),
    UniqueConstraint('citation_target_id', 'citation_target_type', 'citation_reference_id', 'citation_type', 'citation_page_number', 'citation_remarks'),
    Index('citation_citation_target_id_citation_reference_id_idx', 'citation_target_id', 'citation_reference_id')
)


class EntityRelationship(Base):
    __tablename__ = 'entity_relationship'
    __table_args__ = (
        CheckConstraint('entity_relationship_order >= 0'),
    )

    entity_relationship_id = Column(Text, primary_key=True)
    depends_on_entity_relationship_id = Column(ForeignKey('entity_relationship.entity_relationship_id', ondelete='CASCADE', deferrable=True), index=True)
    subject_entity_id = Column(ForeignKey('entity.entity_id', ondelete='CASCADE', deferrable=True), index=True)
    entity_relationship_type = Column(Text, nullable=False)
    object_entity_id = Column(ForeignKey('entity.entity_id', ondelete='CASCADE', deferrable=True), index=True)
    object_entity_iri = Column(Text)
    entity_relationship_date = Column(Text)
    entity_relationship_order = Column(SmallInteger, nullable=False, server_default=text("0"))

    depends_on_entity_relationship = relationship('EntityRelationship', remote_side=[entity_relationship_id])
    object_entity = relationship('Entity', primaryjoin='EntityRelationship.object_entity_id == Entity.entity_id')
    subject_entity = relationship('Entity', primaryjoin='EntityRelationship.subject_entity_id == Entity.entity_id')


class Event(Base):
    __tablename__ = 'event'
    __table_args__ = (
        CheckConstraint('(day >= 1) AND (day <= 31)'),
        CheckConstraint('(month >= 1) AND (month <= 12)')
    )

    event_id = Column(Text, primary_key=True)
    parent_event_id = Column(ForeignKey('event.event_id', ondelete='CASCADE', deferrable=True), index=True)
    dataset_id = Column(Text, nullable=False)
    location_id = Column(ForeignKey('location.location_id', ondelete='CASCADE', deferrable=True), index=True)
    protocol_id = Column(ForeignKey('protocol.protocol_id', ondelete='CASCADE', deferrable=True), index=True)
    event_type = Column(Text, nullable=False)
    event_name = Column(Text)
    field_number = Column(Text)
    event_date = Column(Text)
    year = Column(SmallInteger)
    month = Column(SmallInteger)
    day = Column(SmallInteger)
    verbatim_event_date = Column(Text)
    verbatim_locality = Column(Text)
    verbatim_elevation = Column(Text)
    verbatim_depth = Column(Text)
    verbatim_coordinates = Column(Text)
    verbatim_latitude = Column(Text)
    verbatim_longitude = Column(Text)
    verbatim_coordinate_system = Column(Text)
    verbatim_srs = Column(Text)
    habitat = Column(Text)
    protocol_description = Column(Text)
    sample_size_value = Column(Text)
    sample_size_unit = Column(Text)
    event_effort = Column(Text)
    field_notes = Column(Text)
    event_remarks = Column(Text)

    location = relationship('Location')
    parent_event = relationship('Event', remote_side=[event_id])
    protocol = relationship('Protocol')


class Occurrence(Event):
    __tablename__ = 'occurrence'

    occurrence_id = Column(ForeignKey('event.event_id', ondelete='CASCADE', deferrable=True), primary_key=True)
    organism_id = Column(ForeignKey('organism.organism_id', ondelete='CASCADE', deferrable=True), index=True)
    organism_quantity = Column(Text)
    organism_quantity_type = Column(Text)
    sex = Column(Text)
    life_stage = Column(Text)
    reproductive_condition = Column(Text)
    behavior = Column(Text)
    establishment_means = Column(Enum('NATIVE_INDIGENOUS', 'NATIVE_REINTRODUCED', 'INTRODUCED', 'INTRODUCED_ASSISTED_RECOLONISATION', 'VAGRANT', 'UNCERTAIN', name='establishment_means'))
    occurrence_status = Column(Enum('PRESENT', 'ABSENT', name='occurrence_status'), nullable=False, index=True, server_default=text("'PRESENT'::occurrence_status"))
    pathway = Column(Enum('CORRIDOR_AND_DISPERSAL', 'UNAIDED', 'NATURAL_DISPERSAL', 'CORRIDOR', 'TUNNELS_BRIDGES', 'WATERWAYS_BASINS_SEAS', 'UNINTENTIONAL', 'TRANSPORT_STOWAWAY', 'OTHER_TRANSPORT', 'VEHICLES', 'HULL_FOULING', 'BALLAST_WATER', 'PACKING_MATERIAL', 'PEOPLE', 'MACHINERY_EQUIPMENT', 'HITCHHIKERS_SHIP', 'HITCHHIKERS_AIRPLANE', 'CONTAINER_BULK', 'FISHING_EQUIPMENT', 'TRANSPORT_CONTAMINANT', 'TRANSPORTATION_HABITAT_MATERIAL', 'TIMBER_TRADE', 'SEED_CONTAMINANT', 'PARASITES_ON_PLANTS', 'CONTAMINANT_ON_PLANTS', 'PARASITES_ON_ANIMALS', 'CONTAMINANT_ON_ANIMALS', 'FOOD_CONTAMINANT', 'CONTAMINATE_BAIT', 'CONTAMINANT_NURSERY', 'INTENTIONAL', 'ESCAPE_FROM_CONFINEMENT', 'OTHER_ESCAPE', 'LIVE_FOOD_LIVE_BAIT', 'RESEARCH', 'ORNAMENTAL_NON_HORTICULTURE', 'HORTICULTURE', 'FUR', 'FORESTRY', 'FARMED_ANIMALS', 'PET', 'PUBLIC_GARDEN_ZOO_AQUARIA', 'AQUACULTURE_MARICULTURE', 'AGRICULTURE', 'RELEASE_IN_NATURE', 'OTHER_INTENTIONAL_RELEASE', 'RELEASED_FOR_USE', 'CONSERVATION_OR_WILDLIFE_MANAGEMENT', 'LANDSCAPE_IMPROVEMENT', 'HUNTING', 'FISHERY_IN_THE_WILD', 'EROSION_CONTROL', 'BIOLOGICAL_CONTROL', name='pathway'))
    degree_of_establishment = Column(Enum('MANAGED', 'CAPTIVE', 'CULTIVATED', 'RELEASED', 'UNESTABLISHED', 'FAILING', 'CASUAL', 'NATURALIZED', 'REPRODUCING', 'ESTABLISHED', 'SPREADING', 'WIDESPREAD_INVASIVE', 'COLONISING', 'INVASIVE', 'NATIVE', name='degree_of_establishment'))
    georeference_verification_status = Column(Text)
    occurrence_remarks = Column(Text)
    information_withheld = Column(Text)
    data_generalizations = Column(Text)
    recorded_by = Column(Text)
    recorded_by_id = Column(Text)
    associated_media = Column(Text)
    associated_occurrences = Column(Text)
    associated_taxa = Column(Text)

    organism = relationship('Organism')


t_identification_evidence = Table(
    'identification_evidence', metadata,
    Column('identification_id', ForeignKey('identification.identification_id', ondelete='CASCADE', deferrable=True), primary_key=True, nullable=False),
    Column('entity_id', ForeignKey('entity.entity_id', ondelete='CASCADE', deferrable=True), primary_key=True, nullable=False)
)


class TaxonIdentification(Base):
    __tablename__ = 'taxon_identification'
    __table_args__ = (
        CheckConstraint('taxon_order >= 0'),
    )

    taxon_id = Column(ForeignKey('taxon.taxon_id', ondelete='CASCADE', deferrable=True), primary_key=True, nullable=False)
    identification_id = Column(ForeignKey('identification.identification_id', ondelete='CASCADE', deferrable=True), primary_key=True, nullable=False)
    taxon_order = Column(SmallInteger, primary_key=True, nullable=False, server_default=text("0"))
    taxon_authority = Column(Text)

    identification = relationship('Identification')
    taxon = relationship('Taxon')


class ChronometricAge(Base):
    __tablename__ = 'chronometric_age'

    chronometric_age_id = Column(Text, primary_key=True)
    material_entity_id = Column(ForeignKey('material_entity.material_entity_id', ondelete='CASCADE', deferrable=True), index=True)
    verbatim_chronometric_age = Column(Text)
    verbatim_chronometric_age_protocol = Column(Text)
    uncalibrated_chronometric_age = Column(Text)
    chronometric_age_conversion_protocol = Column(Text)
    earliest_chronometric_age = Column(Integer)
    earliest_chronometric_age_reference_system = Column(Text)
    latest_chronometric_age = Column(Integer)
    latest_chronometric_age_reference_system = Column(Text)
    chronometric_age_uncertainty_in_years = Column(Integer)
    chronometric_age_uncertainty_method = Column(Text)
    material_dated = Column(Text)
    material_dated_id = Column(Text)
    material_dated_relationship = Column(Text)
    chronometric_age_determined_by = Column(Text)
    chronometric_age_determined_date = Column(Text)
    chronometric_age_references = Column(Text)
    chronometric_age_remarks = Column(Text)

    material_entity = relationship('MaterialEntity')


t_occurrence_evidence = Table(
    'occurrence_evidence', metadata,
    Column('occurrence_id', ForeignKey('occurrence.occurrence_id', ondelete='CASCADE', deferrable=True), primary_key=True, nullable=False),
    Column('entity_id', ForeignKey('entity.entity_id', ondelete='CASCADE', deferrable=True), primary_key=True, nullable=False)
)