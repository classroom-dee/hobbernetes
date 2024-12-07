from pyspark import SparkContext

# Initialize SparkContext
sc = SparkContext("local", "RDD Example")

# Create an RDD from a Python list
data = [1, 2, 3, 4, 5]
rdd = sc.parallelize(data)

# Perform transformations
mapped_rdd = rdd.map(lambda x: x * 2)  # Double each element
filtered_rdd = mapped_rdd.filter(lambda x: x >= 5)  # Filter elements >= 5

# Perform actions
result = filtered_rdd.collect()
print("Filtered and Mapped RDD:", result)

# Stop SparkContext
sc.stop()
