# Project rules
- Keep Django's built-in authentication and protect all catalog-management views with server-side login checks, because management data must never be public.
- Keep database settings environment-driven with MySQL/XAMPP defaults and SQLite only for isolated tests, because deployment and testing environments differ.
- Store product media as validated URLs rather than uploaded files, because this project has no configured media storage service.
