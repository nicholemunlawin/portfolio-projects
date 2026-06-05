--
-- PostgreSQL database dump
--

-- Dumped from database version 12.22 (Ubuntu 12.22-0ubuntu0.20.04.4)
-- Dumped by pg_dump version 12.22 (Ubuntu 12.22-0ubuntu0.20.04.4)

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

DROP DATABASE universe;
--
-- Name: universe; Type: DATABASE; Schema: -; Owner: freecodecamp
--

CREATE DATABASE universe WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'C.UTF-8' LC_CTYPE = 'C.UTF-8';


ALTER DATABASE universe OWNER TO freecodecamp;

\connect universe

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
-- Name: blackhole; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.blackhole (
    blackhole_id integer NOT NULL,
    name character varying(50) NOT NULL,
    distance_from_earth integer NOT NULL
);


ALTER TABLE public.blackhole OWNER TO freecodecamp;

--
-- Name: blackhole_blackhole_id_seq; Type: SEQUENCE; Schema: public; Owner: freecodecamp
--

CREATE SEQUENCE public.blackhole_blackhole_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blackhole_blackhole_id_seq OWNER TO freecodecamp;

--
-- Name: blackhole_blackhole_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: freecodecamp
--

ALTER SEQUENCE public.blackhole_blackhole_id_seq OWNED BY public.blackhole.blackhole_id;


--
-- Name: galaxy; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.galaxy (
    galaxy_id integer NOT NULL,
    name character varying(50) NOT NULL,
    has_life boolean,
    galaxy_type character varying(50),
    distance_from_earth integer
);


ALTER TABLE public.galaxy OWNER TO freecodecamp;

--
-- Name: galaxy_galaxy_id_seq; Type: SEQUENCE; Schema: public; Owner: freecodecamp
--

CREATE SEQUENCE public.galaxy_galaxy_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.galaxy_galaxy_id_seq OWNER TO freecodecamp;

--
-- Name: galaxy_galaxy_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: freecodecamp
--

ALTER SEQUENCE public.galaxy_galaxy_id_seq OWNED BY public.galaxy.galaxy_id;


--
-- Name: moon; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.moon (
    moon_id integer NOT NULL,
    name character varying(50) NOT NULL,
    planet_id integer,
    distance_from_earth numeric(15,2),
    is_spherical boolean
);


ALTER TABLE public.moon OWNER TO freecodecamp;

--
-- Name: moon_moon_id_seq; Type: SEQUENCE; Schema: public; Owner: freecodecamp
--

CREATE SEQUENCE public.moon_moon_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.moon_moon_id_seq OWNER TO freecodecamp;

--
-- Name: moon_moon_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: freecodecamp
--

ALTER SEQUENCE public.moon_moon_id_seq OWNED BY public.moon.moon_id;


--
-- Name: planet; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.planet (
    planet_id integer NOT NULL,
    name character varying(50) NOT NULL,
    description text,
    has_life boolean,
    is_spherical boolean,
    star_id integer
);


ALTER TABLE public.planet OWNER TO freecodecamp;

--
-- Name: planet_planet_id_seq; Type: SEQUENCE; Schema: public; Owner: freecodecamp
--

CREATE SEQUENCE public.planet_planet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.planet_planet_id_seq OWNER TO freecodecamp;

--
-- Name: planet_planet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: freecodecamp
--

ALTER SEQUENCE public.planet_planet_id_seq OWNED BY public.planet.planet_id;


--
-- Name: star; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.star (
    star_id integer NOT NULL,
    name character varying(50) NOT NULL,
    distance_from_earth numeric(15,2),
    age_in_millions_of_years integer,
    galaxy_id integer,
    star_type character varying(50)
);


ALTER TABLE public.star OWNER TO freecodecamp;

--
-- Name: star_star_id_seq; Type: SEQUENCE; Schema: public; Owner: freecodecamp
--

CREATE SEQUENCE public.star_star_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.star_star_id_seq OWNER TO freecodecamp;

--
-- Name: star_star_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: freecodecamp
--

ALTER SEQUENCE public.star_star_id_seq OWNED BY public.star.star_id;


--
-- Name: blackhole blackhole_id; Type: DEFAULT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.blackhole ALTER COLUMN blackhole_id SET DEFAULT nextval('public.blackhole_blackhole_id_seq'::regclass);


--
-- Name: galaxy galaxy_id; Type: DEFAULT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.galaxy ALTER COLUMN galaxy_id SET DEFAULT nextval('public.galaxy_galaxy_id_seq'::regclass);


--
-- Name: moon moon_id; Type: DEFAULT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.moon ALTER COLUMN moon_id SET DEFAULT nextval('public.moon_moon_id_seq'::regclass);


--
-- Name: planet planet_id; Type: DEFAULT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.planet ALTER COLUMN planet_id SET DEFAULT nextval('public.planet_planet_id_seq'::regclass);


--
-- Name: star star_id; Type: DEFAULT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.star ALTER COLUMN star_id SET DEFAULT nextval('public.star_star_id_seq'::regclass);


--
-- Data for Name: blackhole; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.blackhole VALUES (1, 'Sagittarius', 26000000);
INSERT INTO public.blackhole VALUES (2, 'Gaia BH1', 1560000);
INSERT INTO public.blackhole VALUES (3, 'Cygnus X-1', 6000000);


--
-- Data for Name: galaxy; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.galaxy VALUES (1, 'Milky Way', true, 'Barred Spiral', 0);
INSERT INTO public.galaxy VALUES (2, 'Andromeda', false, 'Spiral', 2500000);
INSERT INTO public.galaxy VALUES (3, 'Triangulum', false, 'Spiral', 2700000);
INSERT INTO public.galaxy VALUES (4, 'Sombrero', false, 'Unbarred Spiral', 29000000);
INSERT INTO public.galaxy VALUES (5, 'Whirlpool', false, 'Spiral', 31000000);
INSERT INTO public.galaxy VALUES (6, 'Pinwheel', false, 'Spiral', 21000000);


--
-- Data for Name: moon; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.moon VALUES (1, 'Luna', 4, 384000.00, true);
INSERT INTO public.moon VALUES (2, 'Phobos', 5, 9380000.00, true);
INSERT INTO public.moon VALUES (3, 'Deimos', 5, 12380000.00, true);
INSERT INTO public.moon VALUES (4, 'Ganymede', 6, 234580000.00, true);
INSERT INTO public.moon VALUES (5, 'Callisto', 6, 223480000.00, true);
INSERT INTO public.moon VALUES (6, 'Europa', 6, 232480000.00, true);
INSERT INTO public.moon VALUES (7, 'Io', 6, 234580000.00, true);
INSERT INTO public.moon VALUES (8, 'Titan', 7, 585780000.00, true);
INSERT INTO public.moon VALUES (9, 'Enceladus', 7, 547380000.00, true);
INSERT INTO public.moon VALUES (10, 'Titania', 8, 745230000.00, true);
INSERT INTO public.moon VALUES (11, 'Oberon', 8, 795830000.00, true);
INSERT INTO public.moon VALUES (12, 'Triton', 9, 994330000.00, true);
INSERT INTO public.moon VALUES (13, 'Charon', 10, 9943300000.00, true);
INSERT INTO public.moon VALUES (14, 'Kepler-1625b-i', 11, 99433000000.00, true);
INSERT INTO public.moon VALUES (15, 'Kepler-455b-i', 11, 93459876000.00, true);
INSERT INTO public.moon VALUES (16, 'Kepler-1708b-i', 11, 348957344300.00, true);
INSERT INTO public.moon VALUES (17, 'Kepler-34578b-i', 11, 348234897234.00, true);
INSERT INTO public.moon VALUES (18, 'Kepler-4568b-i', 11, 345783645546.00, true);
INSERT INTO public.moon VALUES (19, 'Kepler-85689b-i', 11, 3457634578326.00, true);
INSERT INTO public.moon VALUES (20, 'Kepler-3458b-i', 11, 345892376489.00, true);


--
-- Data for Name: planet; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.planet VALUES (2, 'Mercury', 'Smallest planet', false, true, 1);
INSERT INTO public.planet VALUES (3, 'Venus', 'Hottest planet', false, true, 1);
INSERT INTO public.planet VALUES (4, 'Earth', 'Home planet', true, true, 1);
INSERT INTO public.planet VALUES (5, 'Mars', 'Red planet', false, true, 1);
INSERT INTO public.planet VALUES (6, 'Jupiter', 'Largest planet', false, true, 1);
INSERT INTO public.planet VALUES (7, 'Saturn', 'Famous for its spectacular, wide ring system', false, true, 1);
INSERT INTO public.planet VALUES (8, 'Uranus', 'Ice giant', false, true, 1);
INSERT INTO public.planet VALUES (9, 'Neptune', 'Most distant official planet', false, true, 1);
INSERT INTO public.planet VALUES (10, 'Proxima Centauri b', 'Closest known exoplanet', false, true, 2);
INSERT INTO public.planet VALUES (11, 'Kepler-186f', 'Earth''s cousin', false, true, 2);
INSERT INTO public.planet VALUES (12, 'Kepler-452b', 'Earth like planet', false, true, 2);
INSERT INTO public.planet VALUES (13, '51 Pegasi b', 'First exoplanet confirmed', false, true, 2);


--
-- Data for Name: star; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.star VALUES (1, 'Sun', 149600000.00, 4600, 1, 'G2V');
INSERT INTO public.star VALUES (2, 'Sirius', 8600000000.00, 2, 1, 'A1V');
INSERT INTO public.star VALUES (3, 'Canopus', 310000000000.00, 33, 1, 'F0II');
INSERT INTO public.star VALUES (4, 'Alpha Centauri', 4370000000.00, 5000, 1, 'G2V');
INSERT INTO public.star VALUES (5, 'Arcturus', 370000000000.00, 7100, 1, 'K1.5III');
INSERT INTO public.star VALUES (6, 'Vega', 25000000000.00, 850, 1, 'A0V');


--
-- Name: blackhole_blackhole_id_seq; Type: SEQUENCE SET; Schema: public; Owner: freecodecamp
--

SELECT pg_catalog.setval('public.blackhole_blackhole_id_seq', 3, true);


--
-- Name: galaxy_galaxy_id_seq; Type: SEQUENCE SET; Schema: public; Owner: freecodecamp
--

SELECT pg_catalog.setval('public.galaxy_galaxy_id_seq', 9, true);


--
-- Name: moon_moon_id_seq; Type: SEQUENCE SET; Schema: public; Owner: freecodecamp
--

SELECT pg_catalog.setval('public.moon_moon_id_seq', 20, true);


--
-- Name: planet_planet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: freecodecamp
--

SELECT pg_catalog.setval('public.planet_planet_id_seq', 13, true);


--
-- Name: star_star_id_seq; Type: SEQUENCE SET; Schema: public; Owner: freecodecamp
--

SELECT pg_catalog.setval('public.star_star_id_seq', 6, true);


--
-- Name: blackhole blackhole_name_key; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.blackhole
    ADD CONSTRAINT blackhole_name_key UNIQUE (name);


--
-- Name: blackhole blackhole_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.blackhole
    ADD CONSTRAINT blackhole_pkey PRIMARY KEY (blackhole_id);


--
-- Name: galaxy galaxy_name_constraint; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.galaxy
    ADD CONSTRAINT galaxy_name_constraint UNIQUE (name);


--
-- Name: galaxy galaxy_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.galaxy
    ADD CONSTRAINT galaxy_pkey PRIMARY KEY (galaxy_id);


--
-- Name: moon moon_name_constraint; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.moon
    ADD CONSTRAINT moon_name_constraint UNIQUE (name);


--
-- Name: moon moon_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.moon
    ADD CONSTRAINT moon_pkey PRIMARY KEY (moon_id);


--
-- Name: planet planet_name_constraint; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.planet
    ADD CONSTRAINT planet_name_constraint UNIQUE (name);


--
-- Name: planet planet_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.planet
    ADD CONSTRAINT planet_pkey PRIMARY KEY (planet_id);


--
-- Name: star star_name_constraint; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_name_constraint UNIQUE (name);


--
-- Name: star star_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_pkey PRIMARY KEY (star_id);


--
-- Name: moon moon_planet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.moon
    ADD CONSTRAINT moon_planet_id_fkey FOREIGN KEY (planet_id) REFERENCES public.planet(planet_id);


--
-- Name: planet planet_star_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.planet
    ADD CONSTRAINT planet_star_id_fkey FOREIGN KEY (star_id) REFERENCES public.star(star_id);


--
-- Name: star star_galaxy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_galaxy_id_fkey FOREIGN KEY (galaxy_id) REFERENCES public.galaxy(galaxy_id);


--
-- PostgreSQL database dump complete
--

