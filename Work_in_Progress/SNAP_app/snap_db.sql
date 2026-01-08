--
-- PostgreSQL database dump
--

\restrict j34WRIjyOIzFBRIsa0b0jsCEhvNAafv2iyBSriEIEdkTw7SweglDZu30zIxX5yO

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: backups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.backups (
    backup_id integer NOT NULL,
    device_id integer NOT NULL,
    backup_data text,
    backup_date timestamp with time zone
);


ALTER TABLE public.backups OWNER TO postgres;

--
-- Name: configs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.configs (
    config_id integer NOT NULL,
    device_id integer NOT NULL,
    config_text text,
    created_at timestamp with time zone
);


ALTER TABLE public.configs OWNER TO postgres;

--
-- Name: devices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.devices (
    hostname character varying(100),
    ip_address character varying(30),
    model character varying(50),
    location character varying(50),
    device_id integer NOT NULL
);


ALTER TABLE public.devices ADD COLUMN role VARCHAR(50);

ALTER TABLE public.devices OWNER TO postgres;

--
-- Name: logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logs (
    log_id integer NOT NULL,
    device_id integer NOT NULL,
    log_message text,
    log_date timestamp with time zone
);


ALTER TABLE public.logs OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(20),
    password_hash character varying(255),
    role character varying(20)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: backups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.backups (backup_id, device_id, backup_data, backup_date) FROM stdin;
\.


--
-- Data for Name: configs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.configs (config_id, device_id, config_text, created_at) FROM stdin;
\.


--
-- Data for Name: devices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.devices (hostname, ip_address, model, location, device_id) FROM stdin;
\.


--
-- Data for Name: logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logs (log_id, device_id, log_message, log_date) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, username, password_hash, role) FROM stdin;
\.


--
-- Name: backups backups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.backups
    ADD CONSTRAINT backups_pkey PRIMARY KEY (backup_id);


--
-- Name: configs configs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configs
    ADD CONSTRAINT configs_pkey PRIMARY KEY (config_id);


--
-- Name: devices devices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (device_id);


--
-- Name: logs logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_pkey PRIMARY KEY (log_id);


--
-- Name: users users_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_id PRIMARY KEY (user_id);


--
-- Name: backups backups_device_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.backups
    ADD CONSTRAINT backups_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(device_id);


--
-- Name: configs configs_device_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configs
    ADD CONSTRAINT configs_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(device_id);


--
-- PostgreSQL database dump complete
--

\unrestrict j34WRIjyOIzFBRIsa0b0jsCEhvNAafv2iyBSriEIEdkTw7SweglDZu30zIxX5yO

