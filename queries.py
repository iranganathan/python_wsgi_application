# -*- coding: utf-8 -*-

get_all_regions = """
    SELECT *
    FROM REGION
"""

get_regions_with_feedback_count_greater = """
    SELECT
      REG.NAME AS REGION_NAME
      , REG.ID_REGION AS ID_REGION
      , COUNT(*) AS CNT
    FROM FEEDBACK FDB
      LEFT JOIN REGION AS REG ON FDB.ID_REGION = REG.ID_REGION 
    GROUP BY FDB.ID_REGION
    HAVING CNT > :feedback_count
"""

get_regions_with_feedback_count = """
    WITH FDB AS (
      SELECT
        FDB.ID_REGION AS ID_REGION
        , COUNT(*) AS CNT
      FROM FEEDBACK FDB
      GROUP BY FDB.ID_REGION
    )
    SELECT
      REG.NAME AS REGION_NAME
      , REG.ID_REGION AS ID_REGION
      , FDB.CNT AS CNT
    FROM REGION REG
      LEFT JOIN FDB ON FDB.ID_REGION = REG.ID_REGION
"""

get_all_cities = """
    SELECT
      CIT.ID_CITY
      , CIT.NAME AS CITY_NAME
      , REG.NAME AS REGION_NAME
    FROM CITY CIT
      JOIN REGION REG ON CIT.ID_REGION = REG.ID_REGION
"""

get_all_cities_in_region = """
    SELECT *
    FROM CITY
    WHERE ID_REGION = :id_region
"""

get_cities_and_feedback_count = """
    SELECT
      REG.NAME AS REGION_NAME
      , CIT.NAME AS CITY_NAME
      , CIT.ID_CITY AS ID_CITY
      , COUNT(*) AS CNT
    FROM FEEDBACK FDB
      JOIN REGION AS REG ON FDB.ID_REGION = REG.ID_REGION
      LEFT JOIN CITY AS CIT ON FDB.ID_CITY = CIT.ID_CITY
    GROUP BY FDB.ID_CITY
"""

get_all_feedback = """
    SELECT
      FDB.ID_FEEDBACK AS ID_FEEDBACK
      , FDB.LAST_NAME AS LAST_NAME
      , FDB.FIRST_NAME AS FIRST_NAME
      , REG.NAME AS REGION_NAME
      , CIT.NAME AS CITY_NAME
      , FDB.PHONE AS PHONE
      , FDB.EMAIL AS EMAIL
      , FDB.MESSAGE AS MESSAGE 
    FROM FEEDBACK AS FDB 
      LEFT JOIN REGION AS REG ON FDB.ID_REGION = REG.ID_REGION
      LEFT JOIN CITY AS CIT ON FDB.ID_CITY = CIT.ID_CITY
"""

add_region = """
    INSERT INTO REGION (NAME)
    VALUES (:region_name)
"""

delete_region = """
    DELETE FROM REGION
    WHERE ID_REGION = :id_region
"""

add_city = """
    INSERT INTO CITY (ID_REGION, NAME)
    VALUES (:id_region, :city_name)
"""

delete_city = """
    DELETE FROM CITY
    WHERE ID_CITY = :id_city
"""

add_feedback = """
    INSERT INTO FEEDBACK (LAST_NAME, FIRST_NAME, ID_REGION, ID_CITY, PHONE, EMAIL, MESSAGE)
    VALUES (:last_name, :first_name, :id_region, :id_city, :phone, :email, :message)
"""

delete_feedback = """
    DELETE FROM FEEDBACK
    WHERE ID_FEEDBACK = :id_feedback
"""
