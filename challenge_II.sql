-- CustomerReview

-- CREATE OR REPLACE MODEL `CustomerReview.Embeddings`
-- REMOTE WITH CONNECTION `us.embedding_conn`
-- OPTIONS (ENDPOINT = 'text-embedding-005');

-- LOAD DATA OVERWRITE CustomerReview.customer_reviews
-- (
--     question STRING,
--     answer STRING
-- )
-- FROM FILES (
--     format = 'CSV',
--     uris = ['gs://labs.roitraining.com/aurora-bay-faqs/aurora-bay-faqs.csv']
-- );

-- CREATE OR REPLACE TABLE `CustomerReview.customer_reviews_embedded` AS
-- SELECT *
-- FROM ML.GENERATE_EMBEDDING(
--     MODEL `CustomerReview.Embeddings`,
--     (SELECT review_text AS content FROM `CustomerReview.customer_reviews`)
-- );

-- CREATE OR REPLACE TABLE `CustomerReview.customer_reviews_embedded` AS 
-- SELECT * 
-- FROM ML.GENERATE_EMBEDDING(
--     MODEL `CustomerReview.Embeddings`,
--     (SELECT 
--         *,  -- This includes all existing fields
--         CONCAT('Question: ', question, ' Answer: ', answer) AS content 
--      FROM `CustomerReview.customer_reviews`)
-- );

-- CREATE OR REPLACE TABLE `CustomerReview.vector_search_result` AS
-- SELECT
--     query.query,
--     base.content
-- FROM
--     VECTOR_SEARCH(
--         TABLE `CustomerReview.customer_reviews_embedded`,
--         'ml_generate_embedding_result',
--         (
--             SELECT
--                 ml_generate_embedding_result,
--                 content AS query
--             FROM
--                 ML.GENERATE_EMBEDDING(
--                     MODEL `CustomerReview.Embeddings`,
--                     (SELECT 'service' AS content)
--                 )
--         ),
--         top_k => 5,
--         options => '{"fraction_lists_to_search": 0.01}'
--     );

SELECT
    query.query,
    base.content
FROM
    VECTOR_SEARCH(
        TABLE `CustomerReview.customer_reviews_embedded`,
        'ml_generate_embedding_result',
        (
            SELECT
                ml_generate_embedding_result,
                content AS query
            FROM
                ML.GENERATE_EMBEDDING(
                    MODEL `CustomerReview.Embeddings`,
                    (SELECT 'What are the primary industries in Aurora Bay?' AS content)
                )
        ),
        top_k => 1,
        options => '{"fraction_lists_to_search": 0.01}'
    );
