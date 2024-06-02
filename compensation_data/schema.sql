--
-- PostgreSQL database dump
--
-- Dumped from database version 15.7


--General settings

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Create companies table with associated sequence
--

CREATE TABLE public.companies (
    id integer NOT NULL,
    company_name character varying(255),
    company_size character varying(255),
    industry character varying(255),
    public_or_private character varying(255)
);
ALTER TABLE public.companies OWNER TO postgres;

CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_id_seq OWNER TO postgres;
ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;


--
-- Create compensation table with associated sequence
--

CREATE TABLE public.compensation (
    id integer NOT NULL,
    employee_id integer,
    role_id integer,
    base_salary numeric,
    bonus numeric,
    stock_options numeric,
    currency character varying(10)
);


ALTER TABLE public.compensation OWNER TO postgres;

CREATE SEQUENCE public.compensation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.compensation_id_seq OWNER TO postgres;
ALTER SEQUENCE public.compensation_id_seq OWNED BY public.compensation.id;


--
-- Create employees table with associated sequence
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    age character varying(255),
    gender character varying(255),
    highest_level_of_education character varying(255),
    role_id integer,
    company_id integer,
    location_id integer
);


ALTER TABLE public.employees OWNER TO postgres;
CREATE SEQUENCE public.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE public.employees_id_seq OWNER TO postgres;
ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- Create exchange_rates table
--

CREATE TABLE public.exchange_rates (
    currency character varying(10) NOT NULL,
    rate_to_usd numeric
);


ALTER TABLE public.exchange_rates OWNER TO postgres;

--Create locations table with associated sequence

CREATE TABLE public.locations (
    id integer NOT NULL,
    city character varying(255),
    country character varying(255),
    full_location character varying(255)
);


ALTER TABLE public.locations OWNER TO postgres;
CREATE SEQUENCE public.locations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE public.locations_id_seq OWNER TO postgres;
ALTER SEQUENCE public.locations_id_seq OWNED BY public.locations.id;


--
-- Create roles table with associated sequence
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    job_title character varying(255),
    industry character varying(255),
    employment_type character varying(255)
);


ALTER TABLE public.roles OWNER TO postgres;


CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_id_seq OWNER TO postgres;

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: companies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);


--
-- Name: compensation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compensation ALTER COLUMN id SET DEFAULT nextval('public.compensation_id_seq'::regclass);


--
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- Name: locations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations ALTER COLUMN id SET DEFAULT nextval('public.locations_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);


--
-- Name: compensation compensation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compensation
    ADD CONSTRAINT compensation_pkey PRIMARY KEY (id);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- Name: exchange_rates exchange_rates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exchange_rates
    ADD CONSTRAINT exchange_rates_pkey PRIMARY KEY (currency);


--
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: compensation compensation_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compensation
    ADD CONSTRAINT compensation_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id);


--
-- Name: compensation compensation_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compensation
    ADD CONSTRAINT compensation_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: employees fk_company; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT fk_company FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE SET NULL;


--
-- Name: employees fk_location; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT fk_location FOREIGN KEY (location_id) REFERENCES public.locations(id) ON DELETE SET NULL;


--
-- Name: employees fk_role; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT fk_role FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

