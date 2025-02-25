FROM secoresearch/fuseki:spatial-legacy

# Add custom config file for Fuseki
COPY assembler.ttl $FUSEKI_BASE/configuration/assembler.ttl

# Copy data files
COPY --chown=9008 ttl/*.ttl /tmp/

# Load data into Fuseki and construct indexes
RUN $TDBLOADER --graph=http://ldf.fi/operasampo /tmp/composition_roles.ttl \
    && $TDBLOADER --graph=http://ldf.fi/operasampo /tmp/compositions.ttl \
    && $TDBLOADER --graph=http://ldf.fi/operasampo /tmp/people.ttl \
    && $TDBLOADER --graph=http://ldf.fi/operasampo /tmp/performance_roles.ttl \
    && $TDBLOADER --graph=http://ldf.fi/operasampo /tmp/performances.ttl \
    && $TDBLOADER --graph=http://ldf.fi/operasampo /tmp/places.ttl \
    && $TDBLOADER --graph=http://ldf.fi/operasampo /tmp/producers.ttl \
    && $TEXTINDEXER \
    && $SPATIALINDEXER \
    && $TDBSTATS --graph urn:x-arq:UnionGraph > /tmp/stats.opt \
    && mv /tmp/stats.opt /fuseki-base/databases/tdb/ \
    && rm /tmp/*



