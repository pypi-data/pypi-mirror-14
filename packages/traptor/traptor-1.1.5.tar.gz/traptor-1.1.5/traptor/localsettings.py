'''
Settings for traptor
====================
'''
LOG_LEVEL = 'INFO'

KAFKA_HOSTS = "localhost:9092"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# Kafka topic to write all twitter data
KAFKA_TOPIC = "traptor"

# Your API information.  Fill this out in localsettings.py!
APIKEYS = (
            {
                'CONSUMER_KEY': "BT7iPz8T1EignJYsf7ZU8kIrS",
                'CONSUMER_SECRET': "xxHYJ8eWtO3mGL2AjttIWGEF3w3yErK369bb3rMuBijTeUoEnU",
                'ACCESS_TOKEN': "3515187809-8uT6JFgJFjJDwFlHkBGSd2IE1WQM3IogiDM2yfA",
                'ACCESS_TOKEN_SECRET': "XPgV8byBrP7eGmcV98mWz2MydiGu53Ij4zBQpJGMTA6na"
                },
            {
                'CONSUMER_KEY': "8CqZTWawWLcMWexzjRGvJIz7y",
                'CONSUMER_SECRET': "frHFvSrwH9t8983DhBvFB9Xh7lT3OO0I81cny7t1hiRYf86Oaz",
                'ACCESS_TOKEN': "3515187809-v2K8RL7I1vTt47KJ7vkOfF5H4GGl0Ljf5aEvzUg",
                'ACCESS_TOKEN_SECRET': "7w5PGAAk3YDLTISQaBfJ8TnrmWKIqmcRBdnf2yADAkBtz"
                },
)

'''
Each 'traptor_type' has a unqiue 'traptor_id'.  This ID is how traptor knows
where to look for a ruleset in Redis.  For example, traptor-follow:0
'''

# Options for TRAPTOR_TYPE:  follow, track
TRAPTOR_TYPE = 'track'
TRAPTOR_ID = 0
