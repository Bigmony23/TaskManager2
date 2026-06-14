--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.django_content_type VALUES (1, 'admin', 'logentry');
INSERT INTO public.django_content_type VALUES (2, 'auth', 'permission');
INSERT INTO public.django_content_type VALUES (3, 'auth', 'group');
INSERT INTO public.django_content_type VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO public.django_content_type VALUES (5, 'sessions', 'session');
INSERT INTO public.django_content_type VALUES (6, 'users', 'customuser');
INSERT INTO public.django_content_type VALUES (7, 'task', 'task');
INSERT INTO public.django_content_type VALUES (8, 'task', 'comment');
INSERT INTO public.django_content_type VALUES (9, 'task', 'history');
INSERT INTO public.django_content_type VALUES (10, 'task', 'notification');
INSERT INTO public.django_content_type VALUES (11, 'task', 'project');


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.auth_permission VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO public.auth_permission VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO public.auth_permission VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO public.auth_permission VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO public.auth_permission VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO public.auth_permission VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO public.auth_permission VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO public.auth_permission VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO public.auth_permission VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO public.auth_permission VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO public.auth_permission VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO public.auth_permission VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO public.auth_permission VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO public.auth_permission VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO public.auth_permission VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO public.auth_permission VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO public.auth_permission VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO public.auth_permission VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO public.auth_permission VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO public.auth_permission VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO public.auth_permission VALUES (21, 'Can add user', 6, 'add_customuser');
INSERT INTO public.auth_permission VALUES (22, 'Can change user', 6, 'change_customuser');
INSERT INTO public.auth_permission VALUES (23, 'Can delete user', 6, 'delete_customuser');
INSERT INTO public.auth_permission VALUES (24, 'Can view user', 6, 'view_customuser');
INSERT INTO public.auth_permission VALUES (25, 'Can add task', 7, 'add_task');
INSERT INTO public.auth_permission VALUES (26, 'Can change task', 7, 'change_task');
INSERT INTO public.auth_permission VALUES (27, 'Can delete task', 7, 'delete_task');
INSERT INTO public.auth_permission VALUES (28, 'Can view task', 7, 'view_task');
INSERT INTO public.auth_permission VALUES (29, 'Can add comment', 8, 'add_comment');
INSERT INTO public.auth_permission VALUES (30, 'Can change comment', 8, 'change_comment');
INSERT INTO public.auth_permission VALUES (31, 'Can delete comment', 8, 'delete_comment');
INSERT INTO public.auth_permission VALUES (32, 'Can view comment', 8, 'view_comment');
INSERT INTO public.auth_permission VALUES (33, 'Can add history', 9, 'add_history');
INSERT INTO public.auth_permission VALUES (34, 'Can change history', 9, 'change_history');
INSERT INTO public.auth_permission VALUES (35, 'Can delete history', 9, 'delete_history');
INSERT INTO public.auth_permission VALUES (36, 'Can view history', 9, 'view_history');
INSERT INTO public.auth_permission VALUES (37, 'Can add notification', 10, 'add_notification');
INSERT INTO public.auth_permission VALUES (38, 'Can change notification', 10, 'change_notification');
INSERT INTO public.auth_permission VALUES (39, 'Can delete notification', 10, 'delete_notification');
INSERT INTO public.auth_permission VALUES (40, 'Can view notification', 10, 'view_notification');
INSERT INTO public.auth_permission VALUES (41, 'Can add Проект', 11, 'add_project');
INSERT INTO public.auth_permission VALUES (42, 'Can change Проект', 11, 'change_project');
INSERT INTO public.auth_permission VALUES (43, 'Can delete Проект', 11, 'delete_project');
INSERT INTO public.auth_permission VALUES (44, 'Can view Проект', 11, 'view_project');


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: users_customuser; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.users_customuser VALUES (3, 'pbkdf2_sha256$1000000$82pwWqKcrbAk5UkjYa6E16$B8caEHJwmto7p6GHsEXuEO1frL/Ew4z3qzHHg03JBqM=', '2026-05-29 02:15:01.374493+05', false, 'Manajer1', 'Иван', 'Иванов', 'manager1@gmail.com', false, true, '2026-05-25 06:16:38+05', 'manager', 'Иванович');
INSERT INTO public.users_customuser VALUES (2, 'pbkdf2_sha256$1000000$FZk35XHXv6gkYxcyVxKeYd$KUaX+ciI9RBoZup1lpQICuoR4N2vakjCp85nPJN/ScM=', '2026-05-29 14:21:29.365745+05', false, 'Employee1', 'Антон', 'Иванов', 'emp1@gmail.com', false, true, '2026-05-25 00:47:23+05', 'employee', 'Сергеевич');
INSERT INTO public.users_customuser VALUES (1, 'pbkdf2_sha256$1000000$UnBrfQeDoWLY2joCOia6vA$sltGNNm59sWRtov1niHtHd3JWgUOvaIKpHwTR3SKcPc=', '2026-05-29 14:22:15.219309+05', true, 'Admin', '', '', 'admin@gmail.com', true, true, '2026-05-25 00:38:38+05', 'admin', '');
INSERT INTO public.users_customuser VALUES (6, 'pbkdf2_sha256$1000000$OrG5R2hs05H3ukbLveosS4$J0fyPYhQh+/CjEH/rATqwVkgkJ0Ysa0WB1q67SzK8j0=', NULL, false, 'manager2', 'Дмитрий', 'Козлов', 'manager2@test.com', false, true, '2026-05-28 19:09:01.460066+05', 'manager', 'Александрович');
INSERT INTO public.users_customuser VALUES (7, 'pbkdf2_sha256$1000000$zeZA7tQI9Voe9YlZZKmzM1$cQcX5NYMlDO5ssUZZ+F4rXD2E/kq9RxSzCjV975YoP4=', NULL, false, 'employee3', 'Сергей', 'Морозов', 'emp3@test.com', false, true, '2026-05-28 19:09:01.952078+05', 'employee', 'Викторович');
INSERT INTO public.users_customuser VALUES (8, 'pbkdf2_sha256$1000000$LxWquQYlCHYFFPjT7OqMqG$81mab1URZKOTWLj0NGzZM6Cs80OTOSORiQdpFGgadmM=', NULL, false, 'employee4', 'Анна', 'Волкова', 'emp4@test.com', false, true, '2026-05-28 19:09:02.392206+05', 'employee', 'Сергеевна');
INSERT INTO public.users_customuser VALUES (9, 'pbkdf2_sha256$1000000$Pw8OGL5pi8AqRNCfjM9QWQ$J/aQ22BNLx6w21PZIZpUUuU6zZlKwXeTrLcYZEH0/pc=', NULL, false, 'employee5', 'Николай', 'Лебедев', 'emp5@test.com', false, true, '2026-05-28 19:09:02.836435+05', 'employee', 'Иванович');
INSERT INTO public.users_customuser VALUES (10, 'pbkdf2_sha256$1000000$HT6sbnuU9YTZFr9mkwPUHQ$NP4aH5guBxmrNCr2TYbZb6AAuc80K9pr5vGQML0TIsE=', NULL, false, 'employee6', 'Елена', 'Новикова', 'emp6@test.com', false, true, '2026-05-28 19:09:03.277677+05', 'employee', 'Петровна');
INSERT INTO public.users_customuser VALUES (11, 'pbkdf2_sha256$1000000$nvYbl375k7PHTIYBCWnnfk$05Dc0ebHPJvb7FZHgb5mzcxoje1i+dCSA4Or9DSxEk4=', NULL, false, 'employee7', 'Артём', 'Федоров', 'emp7@test.com', false, true, '2026-05-28 19:09:03.717619+05', 'employee', 'Олегович');
INSERT INTO public.users_customuser VALUES (5, 'pbkdf2_sha256$1000000$16CjdjTLhVsSKBxYaKyCEA$Eok7IhBr1OwX6hgtn3CXytGCRwrA8s0kZDIvqvUIzVA=', NULL, false, 'employee2', 'Мария', 'Сидорова', 'emp2@test.com', false, true, '2026-05-28 04:14:09+05', 'employee', 'Сергеевна');


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.django_admin_log VALUES (1, '2026-05-25 00:47:24.366823+05', '2', 'Антон Сергеевич Иванов', 1, '[{"added": {}}]', 6, 1);
INSERT INTO public.django_admin_log VALUES (2, '2026-05-25 00:47:41.256616+05', '2', 'Антон Сергеевич Иванов', 2, '[]', 6, 1);
INSERT INTO public.django_admin_log VALUES (3, '2026-05-25 00:47:50.211395+05', '2', 'Антон Сергеевич Иванов', 2, '[]', 6, 1);
INSERT INTO public.django_admin_log VALUES (4, '2026-05-25 02:35:16.544197+05', '1', 'Admin', 2, '[{"changed": {"fields": ["Role"]}}]', 6, 1);
INSERT INTO public.django_admin_log VALUES (5, '2026-05-25 05:54:46.220986+05', '2', 'Антон Сергеевич Иванов', 2, '[]', 6, 1);
INSERT INTO public.django_admin_log VALUES (6, '2026-05-25 06:16:39.138937+05', '3', 'Иван Иванов Employee1', 1, '[{"added": {}}]', 6, 1);
INSERT INTO public.django_admin_log VALUES (7, '2026-05-25 06:16:49.148261+05', '3', 'Иван Иванов Employee1', 2, '[{"changed": {"fields": ["Role"]}}]', 6, 1);
INSERT INTO public.django_admin_log VALUES (8, '2026-05-25 06:18:24.964373+05', '3', 'Иван Иванов Employee1', 2, '[]', 6, 1);
INSERT INTO public.django_admin_log VALUES (9, '2026-05-25 08:29:09.64592+05', '2', 'Антон Иванов Сергеевич', 2, '[{"changed": {"fields": ["Last name", "\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e"]}}]', 6, 1);
INSERT INTO public.django_admin_log VALUES (10, '2026-05-28 19:13:27.683094+05', '5', 'Мария Сидорова Сергеевна', 2, '[{"changed": {"fields": ["\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e"]}}]', 6, 1);
INSERT INTO public.django_admin_log VALUES (11, '2026-05-28 19:13:43.02306+05', '4', 'Иван Иванов', 3, '', 6, 1);
INSERT INTO public.django_admin_log VALUES (12, '2026-05-28 21:02:32.067611+05', '3', 'Иван Иванов Иванович', 2, '[{"changed": {"fields": ["\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e"]}}]', 6, 1);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.django_migrations VALUES (1, 'contenttypes', '0001_initial', '2026-05-24 22:54:48.713713+05');
INSERT INTO public.django_migrations VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2026-05-24 22:54:48.719725+05');
INSERT INTO public.django_migrations VALUES (3, 'auth', '0001_initial', '2026-05-24 22:54:48.740709+05');
INSERT INTO public.django_migrations VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2026-05-24 22:54:48.743708+05');
INSERT INTO public.django_migrations VALUES (5, 'auth', '0003_alter_user_email_max_length', '2026-05-24 22:54:48.746714+05');
INSERT INTO public.django_migrations VALUES (6, 'auth', '0004_alter_user_username_opts', '2026-05-24 22:54:48.749713+05');
INSERT INTO public.django_migrations VALUES (7, 'auth', '0005_alter_user_last_login_null', '2026-05-24 22:54:48.751707+05');
INSERT INTO public.django_migrations VALUES (8, 'auth', '0006_require_contenttypes_0002', '2026-05-24 22:54:48.752715+05');
INSERT INTO public.django_migrations VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2026-05-24 22:54:48.754713+05');
INSERT INTO public.django_migrations VALUES (10, 'auth', '0008_alter_user_username_max_length', '2026-05-24 22:54:48.757714+05');
INSERT INTO public.django_migrations VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2026-05-24 22:54:48.759714+05');
INSERT INTO public.django_migrations VALUES (12, 'auth', '0010_alter_group_name_max_length', '2026-05-24 22:54:48.765677+05');
INSERT INTO public.django_migrations VALUES (13, 'auth', '0011_update_proxy_permissions', '2026-05-24 22:54:48.767689+05');
INSERT INTO public.django_migrations VALUES (14, 'auth', '0012_alter_user_first_name_max_length', '2026-05-24 22:54:48.770688+05');
INSERT INTO public.django_migrations VALUES (15, 'users', '0001_initial', '2026-05-24 22:54:48.788771+05');
INSERT INTO public.django_migrations VALUES (16, 'admin', '0001_initial', '2026-05-24 22:54:48.800771+05');
INSERT INTO public.django_migrations VALUES (17, 'admin', '0002_logentry_remove_auto_add', '2026-05-24 22:54:48.803778+05');
INSERT INTO public.django_migrations VALUES (18, 'admin', '0003_logentry_add_action_flag_choices', '2026-05-24 22:54:48.807777+05');
INSERT INTO public.django_migrations VALUES (19, 'sessions', '0001_initial', '2026-05-24 22:54:48.813417+05');
INSERT INTO public.django_migrations VALUES (20, 'task', '0001_initial', '2026-05-24 22:54:48.817422+05');
INSERT INTO public.django_migrations VALUES (21, 'task', '0002_initial', '2026-05-24 22:54:48.827422+05');
INSERT INTO public.django_migrations VALUES (22, 'users', '0002_customuser_patronymic_alter_customuser_role', '2026-05-24 22:54:48.837425+05');
INSERT INTO public.django_migrations VALUES (23, 'task', '0003_task_actual_hours_task_attachments_and_more', '2026-05-25 00:54:40.93426+05');
INSERT INTO public.django_migrations VALUES (24, 'task', '0004_notification', '2026-05-25 07:33:01.917775+05');
INSERT INTO public.django_migrations VALUES (25, 'task', '0005_task_co_executors_task_cost_project_task_project', '2026-05-27 21:40:24.103354+05');
INSERT INTO public.django_migrations VALUES (26, 'task', '0006_alter_task_options_project_actual_hours_and_more', '2026-05-27 22:05:23.862334+05');
INSERT INTO public.django_migrations VALUES (27, 'task', '0007_alter_project_options_remove_project_attachments_and_more', '2026-05-28 01:55:42.732531+05');
INSERT INTO public.django_migrations VALUES (28, 'task', '0008_project_budget_project_client_and_more', '2026-05-28 19:22:36.825385+05');
INSERT INTO public.django_migrations VALUES (29, 'task', '0009_alter_notification_type', '2026-05-28 20:06:43.624038+05');


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.django_session VALUES ('ifnl5uoqojpn5xxfepczyyd2p1jamvsx', '.eJxVjEEOwiAQRe_C2hChQAeX7nsGMjCDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwk7gIJU6_W8T04LoDumO9NZlaXZc5yl2RB-1yasTP6-H-HRTs5VsnHT3ZEaIZVEabPSk3AFlFlEYwA4LhjDoxZnBncsAeLBujHGrFkMT7A_Q9OEg:1wRQAn:uvjlP7CtLP4RiwSn22gx6utk1zYvC8k_2OPwbhULpHc', '2026-06-08 12:56:29.316584+05');
INSERT INTO public.django_session VALUES ('j2su3rjz0s9eqknjs6srx69i7f5ks3cz', '.eJydUMuSmkAU_RfXGQpaYCA7FbQap5tBAZGN1XQ3Q_PSgAbtqfx7ILEqyTaLu7n3PO45n7MTuV2L063n3Umw2deZNvvy9y4jtOLtdGAlaT_OCj23105kygRRntdeQWfG6-UT-49AQfpiZFOQ2cx4tTJ9ruXEyG2mmXOLGRpj9NXS58TSeU4A5SS3TJWZFrctg-u6ZhKgcYuOouVwPRFKed-PevzhFdmGCl94MJJQwwL2sN0ZdAVNWF2SeOXZyghSM3Cts9pWebKsYXkWxwMu0wRLKAaRJsUw7u5YfgzIiQYUIu1t5V2OSSD80p37zmLAzlFDMuphc1HJfhRvXOMI3AEDpOFy8UAyAH4IDT_cVQhAFW-i-TFc11hGYPJgCa5pbV_S6bHSFXmgmLv1fNhW2OnuYdLUxUvT6qqRlt_1MNYr0rEMBdvV9i03o2fsjucd_9Xjf-emTdyMI8lqJDSxPhFQSHXkuBKVlcT7QZDDWv3TRwDw7z6-sU01GRbpJtBTB9390KsRiFTkrAs_LJpj6DUIxAJJV8VhXKSTRxvLNPFychi7FPAOW1VBzu4-XOCjg5ZcnqsNu51huXMXQxIe3hM1kosXT7zH2_3Fmv34Ceb63mU:1wStPz:mWqqPlZm_Mac-HiZHifmzKRxzGj33bymI_3I28r7HP8', '2026-06-12 14:22:15.220915+05');


--
-- Data for Name: task_project; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.task_project VALUES (6, 'Корпоративный портал', 'Разработка внутреннего корпоративного портала для сотрудников компании', 'active', '2026-01-01', '2026-05-30', '2026-05-28 20:00:15.681841+05', '2026-05-28 20:00:15.681841+05', 3, 0, '#667eea', 320, '', 500000, 'ООО Технологии Будущего', 'ДГ-2024/001');
INSERT INTO public.task_project VALUES (2, 'Редизайн сайта ', 'Обновление дизайна и вёрстки сайта', 'active', '2026-05-27', '2026-06-10', '2026-05-27 23:25:19.174692+05', '2026-05-27 23:25:19.174692+05', 3, 0, '#667eea', 0, '', 0, '', '');


--
-- Data for Name: task_task; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.task_task VALUES (22, 'Тестирование системы', 'Нагрузочное и функциональное тестирование', 'new', 2, '2026-05-02 01:48:00+05', '2026-05-28 20:48:45.294948+05', 3, 11, NULL, NULL, '', '2026-05-28 20:48:45.294948+05', 6, NULL, 0);
INSERT INTO public.task_task VALUES (23, 'Написать документацию', 'Техническая документация и руководство пользователя', 'new', 1, '2026-06-05 02:15:30.026622+05', '2026-05-28 21:15:30.027621+05', 3, 2, NULL, NULL, '', '2026-05-28 21:15:30.027621+05', 6, NULL, 0);
INSERT INTO public.task_task VALUES (2, 'Разработка страницы авторизации', 'Создать форму входа с JWT-аутентификацией и обработкой ошибок.', 'done', 3, '2026-05-29 09:28:00+05', '2026-05-25 04:28:57.875382+05', 1, 2, NULL, NULL, '', '2026-05-25 04:29:18.726118+05', NULL, NULL, 0);
INSERT INTO public.task_task VALUES (4, 'Настройка PostgreSQL', 'Подключить базу данных PostgreSQL к Django проекту', 'done', 2, '2026-05-25 12:43:00+05', '2026-05-25 07:43:25.897491+05', 1, 2, NULL, NULL, '', '2026-05-25 07:43:25.897491+05', NULL, NULL, 0);
INSERT INTO public.task_task VALUES (5, 'Создание REST API задач', 'Реализовать CRUD операции для модели Task через DRF.', 'done', 3, '2026-05-28 12:45:00+05', '2026-05-25 07:45:18.63501+05', 1, 2, NULL, NULL, '', '2026-05-25 12:50:09.468721+05', NULL, NULL, 0);
INSERT INTO public.task_task VALUES (6, 'Добавление фильтрации задач', 'Реализовать поиск задач по статусу и приоритету.', 'in_progress', 2, '2026-05-29 13:04:00+05', '2026-05-25 08:04:48.454682+05', 1, 2, NULL, NULL, '', '2026-05-25 12:53:45.730014+05', NULL, NULL, 0);
INSERT INTO public.task_task VALUES (3, 'Реализация Kanban-доски', 'Создать отображение задач по статусам с возможностью фильтрации.', 'done', 1, '2026-05-30 09:30:00+05', '2026-05-25 04:30:26.802955+05', 1, 2, NULL, NULL, '', '2026-05-25 12:54:25.179958+05', NULL, NULL, 0);
INSERT INTO public.task_task VALUES (7, 'Создать дизайн сайта', 'Создать дизайн', 'done', 1, '2026-05-28 17:39:00+05', '2026-05-25 12:39:52.621367+05', 3, 2, NULL, NULL, '', '2026-05-25 15:10:21.523627+05', NULL, NULL, 0);
INSERT INTO public.task_task VALUES (14, 'Верстка сайта', '', 'in_progress', 3, '2026-05-31 05:31:00+05', '2026-05-28 00:31:50.147784+05', 3, 2, NULL, NULL, '', '2026-05-28 02:14:02.505913+05', 2, NULL, 0);
INSERT INTO public.task_task VALUES (18, 'Разработать дизайн главной страницы', 'Создать макет в Figma согласно брендбуку', 'done', 3, '2026-06-05 01:12:56.974712+05', '2026-05-28 20:12:56.97821+05', 3, 2, NULL, NULL, '', '2026-05-28 20:12:56.97821+05', 6, '2026-05-28 20:12:56.974712+05', 0);
INSERT INTO public.task_task VALUES (19, 'Настроить сервер и базу данных', 'Установить nginx, postgresql, настроить бэкап', 'done', 3, '2026-02-16 01:43:00+05', '2026-05-28 20:43:51.06721+05', 3, 5, NULL, NULL, '', '2026-05-28 20:43:51.06721+05', 6, '2026-05-28 20:43:51.06622+05', 0);
INSERT INTO public.task_task VALUES (20, 'Разработать модуль авторизации', 'SSO интеграция с Active Directory', 'in_progress', 3, '2026-04-02 01:45:00+05', '2026-05-28 20:45:47.851871+05', 3, 10, NULL, NULL, '', '2026-05-28 20:45:47.851871+05', 6, NULL, 0);
INSERT INTO public.task_task VALUES (21, 'Разработать новостной модуль', 'Лента новостей с категориями и поиском', 'in_progress', 2, '2026-06-05 01:47:18.702429+05', '2026-05-28 20:47:18.702947+05', 3, 11, NULL, NULL, '', '2026-05-28 20:47:18.702947+05', 6, NULL, 0);


--
-- Data for Name: task_comment; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.task_comment VALUES (1, 'Все ок', '2026-05-25 04:41:42.33841+05', 3, 1);
INSERT INTO public.task_comment VALUES (2, 'Все ок', '2026-05-25 04:42:14.186635+05', 2, 1);
INSERT INTO public.task_comment VALUES (3, 'ок', '2026-05-25 04:42:54.630981+05', 2, 1);
INSERT INTO public.task_comment VALUES (4, 'Да все ок
', '2026-05-25 06:01:58.72746+05', 3, 2);
INSERT INTO public.task_comment VALUES (5, 'Ок', '2026-05-25 06:02:21.915536+05', 2, 2);
INSERT INTO public.task_comment VALUES (6, 'ок', '2026-05-25 12:32:08.997225+05', 5, 2);
INSERT INTO public.task_comment VALUES (7, 'Ок', '2026-05-28 00:33:37.544625+05', 14, 2);
INSERT INTO public.task_comment VALUES (8, 'ок', '2026-05-28 22:05:44.816565+05', 23, 2);
INSERT INTO public.task_comment VALUES (9, 'ок
', '2026-05-28 22:13:44.972733+05', 18, 2);
INSERT INTO public.task_comment VALUES (10, 'ок', '2026-05-28 22:19:10.946926+05', 23, 2);


--
-- Data for Name: task_history; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.task_history VALUES (1, 'in_progress', 'new', '2026-05-25 08:21:02.068251+05', 1, 3);
INSERT INTO public.task_history VALUES (2, 'new', 'in_progress', '2026-05-25 12:33:09.815966+05', 2, 3);
INSERT INTO public.task_history VALUES (3, 'in_progress', 'new', '2026-05-25 12:44:49.145357+05', 1, 6);
INSERT INTO public.task_history VALUES (4, 'new', 'in_progress', '2026-05-25 12:49:47.966585+05', 2, 5);
INSERT INTO public.task_history VALUES (5, 'in_progress', 'done', '2026-05-25 12:50:09.473267+05', 2, 5);
INSERT INTO public.task_history VALUES (6, 'new', 'in_progress', '2026-05-25 12:53:45.733013+05', 3, 6);
INSERT INTO public.task_history VALUES (7, 'in_progress', 'done', '2026-05-25 12:54:25.183141+05', 3, 3);
INSERT INTO public.task_history VALUES (8, 'new', 'in_progress', '2026-05-25 15:10:02.358333+05', 2, 7);
INSERT INTO public.task_history VALUES (9, 'in_progress', 'done', '2026-05-25 15:10:21.530628+05', 2, 7);
INSERT INTO public.task_history VALUES (10, 'new', 'in_progress', '2026-05-28 02:14:02.512265+05', 3, 14);


--
-- Data for Name: task_notification; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.task_notification VALUES (2, 'assigned', 'Задача «Добавление фильтрации задач» назначена на Антон Сергеевич Иванов', true, '2026-05-25 08:04:48.460682+05', 6, 1);
INSERT INTO public.task_notification VALUES (7, 'assigned', 'Задача «Создать дизайн сайта» назначена на Антон Иванов Сергеевич', true, '2026-05-25 12:39:52.625912+05', 7, 3);
INSERT INTO public.task_notification VALUES (15, 'status_changed', 'Задача «Создать дизайн сайта»: Новая → В процессе', true, '2026-05-25 15:10:02.353501+05', 7, 3);
INSERT INTO public.task_notification VALUES (50, 'assigned', '📋 Вам назначена задача: «Тестирование системы»', false, '2026-05-28 20:48:45.306154+05', 22, 11);
INSERT INTO public.task_notification VALUES (16, 'status_changed', 'Задача «Создать дизайн сайта»: В процессе → Завершена', true, '2026-05-25 15:10:21.527722+05', 7, 3);
INSERT INTO public.task_notification VALUES (51, 'assigned', '✅ Задача «Тестирование системы» назначена на Артём Федоров Олегович', true, '2026-05-28 20:48:45.307205+05', 22, 3);
INSERT INTO public.task_notification VALUES (4, 'commented', 'Новый комментарий к задаче «Создание REST API задач» от Антон Иванов Сергеевич', true, '2026-05-25 12:32:09.000214+05', 5, 1);
INSERT INTO public.task_notification VALUES (5, 'status_changed', 'Задача «Реализация Kanban-доски»: Новая → В процессе', true, '2026-05-25 12:33:09.814953+05', 3, 1);
INSERT INTO public.task_notification VALUES (9, 'status_changed', 'Задача «Создание REST API задач»: Новая → В процессе', true, '2026-05-25 12:49:47.965594+05', 5, 1);
INSERT INTO public.task_notification VALUES (10, 'status_changed', 'Задача «Создание REST API задач»: В процессе → Завершена', true, '2026-05-25 12:50:09.471726+05', 5, 1);
INSERT INTO public.task_notification VALUES (11, 'status_changed', 'Задача «Добавление фильтрации задач»: Новая → В процессе', true, '2026-05-25 12:53:45.732014+05', 6, 1);
INSERT INTO public.task_notification VALUES (13, 'status_changed', 'Задача «Реализация Kanban-доски»: В процессе → Завершена', true, '2026-05-25 12:54:25.181134+05', 3, 1);
INSERT INTO public.task_notification VALUES (41, 'assigned', '👥 Вас добавили соисполнителем в задачу: «Разработать дизайн главной страницы»', false, '2026-05-28 20:12:56.997378+05', 18, 9);
INSERT INTO public.task_notification VALUES (3, 'status_changed', 'Задача «Реализация Kanban-доски»: В процессе → Новая', true, '2026-05-25 08:21:02.065282+05', 3, 2);
INSERT INTO public.task_notification VALUES (1, 'assigned', 'Вам назначена задача: «Добавление фильтрации задач»', true, '2026-05-25 08:04:48.457692+05', 6, 2);
INSERT INTO public.task_notification VALUES (6, 'assigned', 'Вам назначена задача: «Создать дизайн сайта»', true, '2026-05-25 12:39:52.623895+05', 7, 2);
INSERT INTO public.task_notification VALUES (8, 'status_changed', 'Задача «Добавление фильтрации задач»: В процессе → Новая', true, '2026-05-25 12:44:49.143005+05', 6, 2);
INSERT INTO public.task_notification VALUES (12, 'status_changed', 'Задача «Добавление фильтрации задач»: Новая → В процессе', true, '2026-05-25 12:53:45.733013+05', 6, 2);
INSERT INTO public.task_notification VALUES (14, 'status_changed', 'Задача «Реализация Kanban-доски»: В процессе → Завершена', true, '2026-05-25 12:54:25.182141+05', 3, 2);
INSERT INTO public.task_notification VALUES (42, 'assigned', '📋 Вам назначена задача: «Настроить сервер и базу данных»', false, '2026-05-28 20:43:51.079973+05', 19, 5);
INSERT INTO public.task_notification VALUES (44, 'assigned', '👥 Вас добавили соисполнителем в задачу: «Настроить сервер и базу данных»', false, '2026-05-28 20:43:51.082979+05', 19, 8);
INSERT INTO public.task_notification VALUES (45, 'assigned', '📋 Вам назначена задача: «Разработать модуль авторизации»', false, '2026-05-28 20:45:47.86288+05', 20, 10);
INSERT INTO public.task_notification VALUES (47, 'assigned', '📋 Вам назначена задача: «Разработать новостной модуль»', false, '2026-05-28 20:47:18.715194+05', 21, 11);
INSERT INTO public.task_notification VALUES (49, 'assigned', '👥 Вас добавили соисполнителем в задачу: «Разработать новостной модуль»', false, '2026-05-28 20:47:18.718209+05', 21, 7);
INSERT INTO public.task_notification VALUES (52, 'assigned', '👥 Вас добавили соисполнителем в задачу: «Тестирование системы»', false, '2026-05-28 20:48:45.308224+05', 22, 6);
INSERT INTO public.task_notification VALUES (39, 'assigned', '📋 Вам назначена задача: «Разработать дизайн главной страницы»', true, '2026-05-28 20:12:56.994377+05', 18, 2);
INSERT INTO public.task_notification VALUES (29, 'assigned', '📋 Вам назначена задача: «Верстка сайта»', true, '2026-05-28 00:31:50.157785+05', 14, 2);
INSERT INTO public.task_notification VALUES (32, 'status_changed', '📌 Задача «Верстка сайта»: 🟡 Новая → 🔵 В процессе', true, '2026-05-28 02:14:02.511266+05', 14, 2);
INSERT INTO public.task_notification VALUES (53, 'assigned', '📋 Вам назначена задача: «Написать документацию»', true, '2026-05-28 21:15:30.038622+05', 23, 2);
INSERT INTO public.task_notification VALUES (56, 'commented', '💬 Новый комментарий к задаче «Разработать дизайн главной страницы» от Employee1', false, '2026-05-28 22:13:44.978746+05', 18, 9);
INSERT INTO public.task_notification VALUES (30, 'assigned', '✅ Задача «Верстка сайта» назначена на Антон Иванов Сергеевич', true, '2026-05-28 00:31:50.157785+05', 14, 3);
INSERT INTO public.task_notification VALUES (31, 'commented', '💬 Новый комментарий к задаче «Верстка сайта» от Employee1', true, '2026-05-28 00:33:37.546712+05', 14, 3);
INSERT INTO public.task_notification VALUES (40, 'assigned', '✅ Задача «Разработать дизайн главной страницы» назначена на Антон Иванов Сергеевич', true, '2026-05-28 20:12:56.995377+05', 18, 3);
INSERT INTO public.task_notification VALUES (43, 'assigned', '✅ Задача «Настроить сервер и базу данных» назначена на Мария Сидорова Сергеевна', true, '2026-05-28 20:43:51.08098+05', 19, 3);
INSERT INTO public.task_notification VALUES (46, 'assigned', '✅ Задача «Разработать модуль авторизации» назначена на Елена Новикова Петровна', true, '2026-05-28 20:45:47.863883+05', 20, 3);
INSERT INTO public.task_notification VALUES (48, 'assigned', '✅ Задача «Разработать новостной модуль» назначена на Артём Федоров Олегович', true, '2026-05-28 20:47:18.716218+05', 21, 3);
INSERT INTO public.task_notification VALUES (54, 'assigned', '✅ Задача «Написать документацию» назначена на Антон Иванов Сергеевич', true, '2026-05-28 21:15:30.039622+05', 23, 3);
INSERT INTO public.task_notification VALUES (55, 'commented', '💬 Новый комментарий к задаче «Написать документацию» от Employee1', true, '2026-05-28 22:05:44.820364+05', 23, 3);
INSERT INTO public.task_notification VALUES (57, 'commented', '💬 Новый комментарий к задаче «Разработать дизайн главной страницы» от Employee1', true, '2026-05-28 22:13:44.979733+05', 18, 3);
INSERT INTO public.task_notification VALUES (58, 'commented', '💬 Новый комментарий к задаче «Написать документацию» от Антон Иванов', true, '2026-05-28 22:19:10.951928+05', 23, 3);


--
-- Data for Name: task_project_members; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.task_project_members VALUES (2, 2, 2);
INSERT INTO public.task_project_members VALUES (9, 6, 1);
INSERT INTO public.task_project_members VALUES (10, 6, 3);
INSERT INTO public.task_project_members VALUES (11, 6, 2);
INSERT INTO public.task_project_members VALUES (13, 6, 9);
INSERT INTO public.task_project_members VALUES (14, 6, 5);
INSERT INTO public.task_project_members VALUES (16, 6, 8);
INSERT INTO public.task_project_members VALUES (17, 6, 10);
INSERT INTO public.task_project_members VALUES (19, 6, 11);
INSERT INTO public.task_project_members VALUES (21, 6, 7);
INSERT INTO public.task_project_members VALUES (24, 6, 6);


--
-- Data for Name: task_task_co_executors; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.task_task_co_executors VALUES (1, 18, 9);
INSERT INTO public.task_task_co_executors VALUES (2, 19, 8);
INSERT INTO public.task_task_co_executors VALUES (3, 21, 7);
INSERT INTO public.task_task_co_executors VALUES (4, 22, 6);


--
-- Data for Name: users_customuser_groups; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: users_customuser_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 44, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 12, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 11, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 29, true);


--
-- Name: task_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.task_comment_id_seq', 10, true);


--
-- Name: task_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.task_history_id_seq', 10, true);


--
-- Name: task_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.task_notification_id_seq', 58, true);


--
-- Name: task_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.task_project_id_seq', 6, true);


--
-- Name: task_project_members_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.task_project_members_id_seq', 26, true);


--
-- Name: task_task_co_executors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.task_task_co_executors_id_seq', 4, true);


--
-- Name: task_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.task_task_id_seq', 23, true);


--
-- Name: users_customuser_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_customuser_groups_id_seq', 1, false);


--
-- Name: users_customuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_customuser_id_seq', 11, true);


--
-- Name: users_customuser_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_customuser_user_permissions_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

