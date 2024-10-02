--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

-- Started on 2024-10-03 00:50:27

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
-- TOC entry 216 (class 1259 OID 39584)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    full_name character varying(100) NOT NULL,
    role character varying(10),
    group_number character(10),
    c_group_1 character(10),
    c_group_2 character(10)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 39583)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 4841 (class 0 OID 0)
-- Dependencies: 215
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4688 (class 2604 OID 39587)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4835 (class 0 OID 39584)
-- Dependencies: 216
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, user_id, full_name, role, group_number, c_group_1, c_group_2) FROM stdin;
1	451218809	Иванов	freshman	С22-712   	\N	\N
2	451218810	Петров	freshman	С22-712   	\N	\N
3	451218811	Сидоров	freshman	С22-712   	\N	\N
6	451218814	Романов	freshman	С22-713   	\N	\N
7	451218815	Соловьёв	freshman	С22-713   	\N	\N
10	451218818	Ефимова	freshman	С22-713   	\N	\N
4	451218812	Кузнецов	curator	С22-712   	С22-713\n  	\N
5	451218813	Смирнова	curator	С22-712   	С22-713   	\N
8	451218816	Орлова	curator	С22-713   	С22-712   	\N
9	451218817	Волкова	curator	С22-713   	С22-712   	\N
15	7151204997	Main Admin	admin	\N	\N	\N
24	547136732	цуц апап фсф	admin	Б22-434   	Б22-900   	С33-000   
25	451218808	Антипенко	freshman	С22-712   	\N	\N
\.


--
-- TOC entry 4842 (class 0 OID 0)
-- Dependencies: 215
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 25, true);


--
-- TOC entry 4690 (class 2606 OID 39589)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id, user_id);


-- Completed on 2024-10-03 00:50:28

--
-- PostgreSQL database dump complete
--

