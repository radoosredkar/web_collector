import sentry_sdk

sentry_sdk.init(
    "https://c457a3b783ea4c2ca406263f30086806@o371271.ingest.sentry.io/5556585",
        traces_sample_rate=1.0
        )

print(1/0)
