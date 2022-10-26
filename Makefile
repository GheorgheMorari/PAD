start_all:
	cd AuthService/ && $(MAKE) start_mongo
	cd MessagingService/ && $(MAKE) start_postgres
