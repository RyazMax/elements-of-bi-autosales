CREATE TABLE mrjazanov_338247.ibd_sales_autodoc ON CLUSTER kube_clickhouse_cluster
(
    `date` DateTime,
    `article_id` Int64,
    `category_id` Int64,
    `sales_operation` String,
    `promotion_percent` Int64,
    `netto_total` Float64,
    `quantity` Int64
)
ENGINE = AggregatingMergeTree
ORDER BY (date, article_id, category_id, sales_operation)

CREATE TABLE mrjazanov_338247.ibd_dist_sales_autodoc ON CLUSTER kube_clickhouse_cluster AS mrjazanov_338247.ibd_sales_autodoc
ENGINE = Distributed(kube_clickhouse_cluster, mrjazanov_338247, ibd_sales_autodoc, intHash64(article_id))