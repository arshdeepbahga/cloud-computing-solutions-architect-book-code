-- Performs function on the aggregate rows over a 10 second 
--   sliding window for specified columns. 
--          .----------.   .----------.   .----------.              
--          |  SOURCE  |   |  INSERT  |   |  DESTIN. |              
-- Source-->|  STREAM  |-->| & SELECT |-->|  STREAM  |-->Destination
--          |          |   |  (PUMP)  |   |          |              
--          '----------'   '----------'   '----------'               
-- STREAM (in-application): a continuously updated entity that you can 
--   SELECT from and INSERT into like a TABLE
-- PUMP: an entity used to continuously 'SELECT ... FROM' a source STREAM,
--   and INSERT SQL results into an output STREAM
-- Create output stream, which can be used to send to a destination

CREATE OR REPLACE STREAM "inapp_stream" (
    "stationID" VARCHAR(8),  
    "pm2_5_avg"     DOUBLE,
    "pm10_avg"     DOUBLE,
    "co_avg"     DOUBLE,
    "so2_avg"     DOUBLE
    );
CREATE OR REPLACE PUMP "STREAM_PUMP" AS 
    INSERT INTO "inapp_stream"
    SELECT STREAM "stationID",       
        AVG("pm2_5") OVER W1 AS "pm2_5_avg",
        AVG("pm10") OVER W1 AS "pm10_avg",
        AVG("co") OVER W1 AS "co_avg",
        AVG("so2") OVER W1 AS "so2_avg"
    FROM "SOURCE_SQL_STREAM_001"
    WINDOW W1 AS (
        PARTITION BY "stationID" 
        RANGE INTERVAL '10' SECOND PRECEDING);