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
