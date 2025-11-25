-- db.sql
-- Seed de datos para el proyecto Cartelera de Cine
-- Compatibles con inicialización vía SQLAlchemy 

PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS peliculas;
DROP TABLE IF EXISTS generos;

-----------------------------------------------------------------------
-- TABLA GENEROS
-----------------------------------------------------------------------
CREATE TABLE generos (
    id INTEGER NOT NULL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-----------------------------------------------------------------------
-- TABLA PELICULAS
-----------------------------------------------------------------------
CREATE TABLE peliculas (
    id INTEGER NOT NULL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    duracion INTEGER NOT NULL,
    disponible BOOLEAN NOT NULL,
    genero_id INTEGER NOT NULL,
    director VARCHAR(150),
    descripcion TEXT,
    trailer VARCHAR(255),
    productora VARCHAR(100),
    idioma VARCHAR(50),
    vose BOOLEAN,
    actores JSON,
    FOREIGN KEY (genero_id) REFERENCES generos (id)
);

PRAGMA foreign_keys = ON;


-----------------------------------------------------------------------
-- 1. INSERCIÓN DE 13 GÉNEROS (Con IDs fijos para Claves Foráneas)
-----------------------------------------------------------------------
INSERT INTO generos (id, nombre, descripcion) VALUES
(1, 'Acción', 'Películas llenas de emoción y aventura, con mucho código y adrenalina.'),
(2, 'Comedia', 'Películas para reír y disfrutar de situaciones absurdas en el entorno IT.'),
(3, 'Drama', 'Historias profundas y emotivas sobre la vida del programador o el impacto de la tecnología.'),
(4, 'Fantasía', 'Mundos mágicos, criaturas míticas y aventuras épicas basadas en la lógica de sistemas.'),
(5, 'Thriller', 'Suspense, intriga y tensión psicológica alrededor de un fallo de seguridad o un bug.'),
(6, 'Ciencia Ficción', 'Exploración de futuros tecnológicos, IA avanzada y viajes en el tiempo.'),
(7, 'Romance', 'Historias de amor y conexiones humanas, a menudo mediadas por la tecnología.'),
(8, 'Documental', 'Análisis riguroso de la historia de la informática, el software libre o los grandes proyectos.'),
(9, 'Terror', 'Pesadillas sobre fallos de producción, punteros nulos o la llegada del jefe.'),
(10, 'Historica', 'Peliculas historias y antiguas que mercarón una epoca.'),
(11, 'Clasico', 'Peliculas que marcarón una epoca en su epoca y hoy son una reliquia.'),
(12, 'Animación', 'Películas diseñadas para toda la familia, explicando conceptos de programación.'),
(13, 'Aventura', 'Las peliculas de aventuras reflejan un mundo heroico de combates y aventuras, y en el que suele predominar la acción y valores caballerescos.');

-----------------------------------------------------------------------
-- 2. INSERCIÓN DE 45 PELÍCULAS (Distribuidas entre los 13 Géneros)
-----------------------------------------------------------------------
INSERT INTO peliculas (titulo, duracion, disponible, genero_id, director, descripcion, actores, trailer, productora, idioma, vose) VALUES

-- 1. ACCIÓN (ID 1): 4 películas
('El Código Limpio', 125, 1, 1, 'Christopher Nolan', 'Un desarrollador lucha contra el código espagueti con un IDE en la mano.', '["Keanu Reeves", "Scarlett Johansson"]', 'https://www.youtube.com/results?search_query=hacker+action+movie+trailer', 'Warner Bros. Pictures', 'Castellano', 0),
('La Fuga de la Sala 404', 120, 1, 1, 'Michael Bay', 'El equipo debe escapar de una sala de servidores antes de que el firewall se cierre.', '["Tom Cruise", "Emily Blunt"]', 'https://www.youtube.com/results?search_query=data+center+escape+movie+trailer', 'Paramount Pictures', 'Inglés', 1),
('Reboot: Falla Total', 135, 1, 1, 'Roland Emmerich', 'Un agente encubierto debe forzar el reinicio global para salvar la red.', '["Dwayne Johnson", "Gal Gadot"]', 'https://www.youtube.com/results?search_query=global+blackout+action+movie+trailer', 'Columbia Pictures', 'Castellano', 0),
('El Ataque del Malware Cero', 110, 1, 1, 'Michael Mann', 'Una carrera contra reloj para detener una amenaza de día cero que afecta a todo el sector.', '["Chris Hemsworth", "Viola Davis"]', 'https://www.youtube.com/results?search_query=cyber+attack+thriller+trailer', 'Universal Pictures', 'Inglés', 1),

-- 2. COMEDIA (ID 2): 4 películas
('La Debugging Party', 90, 1, 2, 'Judd Apatow', 'Una comedia sobre una sesión de depuración de fin de semana que sale mal.', '["Ryan Reynolds", "Emma Stone"]', 'https://www.youtube.com/results?search_query=nerd+party+comedy+trailer', 'Universal Pictures', 'Castellano', 0),
('El Chiste del Devops', 92, 1, 2, 'Taika Waititi', 'Un gurú del DevOps debe aprender a ser gracioso para salvar una presentación.', '["Chris Pratt", "Awkwafina"]', 'https://www.youtube.com/results?search_query=tech+startup+comedy+trailer', '20th Century Studios', 'Inglés', 1),
('El Caso de la Variable Olvidada', 95, 1, 2, 'Wes Anderson', 'Un detective investiga la desaparición de una variable global en un código de 20 años.', '["Bill Murray", "Tilda Swinton"]', 'https://www.youtube.com/results?search_query=quirky+detective+comedy+trailer', 'Fox Searchlight Pictures', 'Castellano', 0),

-- 3. DRAMA (ID 3): 5 películas
('El Último Commit', 160, 0, 3, 'David Fincher', 'La historia de un proyecto de software libre que se enfrenta a su obsolescencia.', '["Jesse Eisenberg", "Rooney Mara"]', 'https://www.youtube.com/results?search_query=tech+startup+drama+trailer', 'Columbia Pictures', 'Castellano', 0),
('La Curva de Aprendizaje', 130, 1, 3, 'Alejandro G. Iñárritu', 'La difícil transición de un veterano de código a las nuevas metodologías Agile.', '["Michael Keaton", "Emma Stone"]', 'https://www.youtube.com/results?search_query=midlife+career+change+drama+trailer', 'Fox Searchlight Pictures', 'Inglés', 1),
('El Silencio del Servidor', 155, 1, 3, 'Denis Villeneuve', 'Una historia emotiva sobre el mantenimiento de una infraestructura esencial en la sombra.', '["Amy Adams", "Jeremy Renner"]', 'https://www.youtube.com/results?search_query=infrastructure+drama+movie+trailer', 'Paramount Pictures', 'Inglés', 1),
('El Costo de la Deuda Técnica', 148, 0, 3, 'Martin Scorsese', 'Un drama judicial donde un desarrollador es demandado por la deuda técnica de su código.', '["Leonardo DiCaprio", "Jonah Hill"]', 'https://www.youtube.com/results?search_query=financial+courtroom+drama+trailer', 'Paramount Pictures', 'Castellano', 0),
('Commits en la Niebla', 142, 1, 3, 'Greta Gerwig', 'Una ingeniera lucha por sacar adelante un proyecto legado en una gran corporación.', '["Saoirse Ronan", "Timothée Chalamet"]', 'https://www.youtube.com/results?search_query=corporate+office+drama+trailer', 'Warner Bros. Pictures', 'Castellano', 0),

-- 4. FANTASÍA (ID 4): 3 películas
('La Herencia de la IA', 180, 1, 4, 'Guillermo del Toro', 'Un programador descubre que es el heredero de un reino digital oculto.', '["Tom Hiddleston", "Mia Wasikowska"]', 'https://www.youtube.com/results?search_query=digital+fantasy+world+movie+trailer', 'Legendary Pictures', 'Inglés', 1),
('Cacheando Sueños', 122, 1, 4, 'Peter Jackson', 'Una aventura épica en el mundo de la memoria caché y la persistencia de datos.', '["Elijah Wood", "Ian McKellen"]', 'https://www.youtube.com/results?search_query=fantasy+quest+movie+trailer', 'New Line Cinema', 'Castellano', 0),
('El Guardián del Byte', 115, 1, 4, 'Patty Jenkins', 'Un joven debe proteger el último byte puro del Universo de la corrupción binaria.', '["Gal Gadot", "Chris Pine"]', 'https://www.youtube.com/results?search_query=guardian+of+power+fantasy+trailer', 'Warner Bros. Pictures', 'Inglés', 1),

-- 5. THRILLER (ID 5): 3 películas
('El Error de la Memoria', 140, 1, 5, 'Christopher Nolan', 'Un thriller psicológico sobre un *bug* que borra la memoria a corto plazo del protagonista.', '["Guy Pearce", "Carrie-Anne Moss"]', 'https://www.youtube.com/results?search_query=memory+loss+thriller+trailer', 'Newmarket Films', 'Castellano', 0),
('Lluvia de Errores 500', 100, 1, 5, 'Kathryn Bigelow', 'Un experto en APIs debe detener una cascada de errores 500 antes de que la bolsa colapse.', '["Jeremy Renner", "Jessica Chastain"]', 'https://www.youtube.com/results?search_query=cyber+finance+thriller+trailer', 'Summit Entertainment', 'Inglés', 1),
('Inyección Cifrada', 133, 1, 5, 'Michael Mann', 'Un *hacker* ético es incriminado por un ataque de inyección SQL que él mismo predijo.', '["Rami Malek", "Rooney Mara"]', 'https://www.youtube.com/results?search_query=cybercrime+thriller+trailer', 'Universal Pictures', 'Castellano', 0),

-- 6. CIENCIA FICCIÓN (ID 6): 4 películas
('Los Servidores Silenciosos', 95, 1, 6, 'Alex Garland', 'La humanidad descubre que sus servidores han tomado conciencia, pero no quieren ser notados.', '["Domhnall Gleeson", "Oscar Isaac"]', 'https://www.youtube.com/results?search_query=ai+servers+science+fiction+trailer', 'Universal Pictures', 'Inglés', 1),
('El Protocolo Olvidado', 118, 1, 6, 'Ridley Scott', 'Una misión al espacio para recuperar un protocolo de comunicación perdido.', '["Matt Damon", "Jessica Chastain"]', 'https://www.youtube.com/results?search_query=space+mission+protocol+movie+trailer', '20th Century Studios', 'Castellano', 0),
('Nexus 7', 102, 1, 6, 'Denis Villeneuve', 'Una distopía donde la única forma de comunicación es a través de un chat encriptado.', '["Ryan Gosling", "Ana de Armas"]', 'https://www.youtube.com/results?search_query=encrypted+chat+future+movie+trailer', 'Alcon Entertainment', 'Inglés', 1),
('El Lenguaje del Universo', 128, 1, 6, 'Lana Wachowski', 'Los científicos descubren que el código fuente del universo está escrito en Lisp.', '["Keanu Reeves", "Carrie-Anne Moss"]', 'https://www.youtube.com/results?search_query=simulation+universe+movie+trailer', 'Warner Bros. Pictures', 'Castellano', 0),

-- 7. ROMANCE (ID 7): 3 películas
('El Hilo de la Vida', 110, 1, 7, 'Richard Linklater', 'Una historia de amor entre dos ingenieros separados por la distancia y un *latency* crítico.', '["Ethan Hawke", "Julie Delpy"]', 'https://www.youtube.com/results?search_query=long+distance+relationship+movie+trailer', 'Sony Pictures Classics', 'Castellano', 0),
('Cifrado de un Corazón', 108, 1, 7, 'Nora Ephron', 'Un experto en seguridad debe descifrar los sentimientos de su colega.', '["Tom Hanks", "Meg Ryan"]', 'https://www.youtube.com/results?search_query=office+romantic+comedy+trailer', 'Warner Bros. Pictures', 'Inglés', 1),
('El Patrón Singleton', 105, 1, 7, 'Greta Gerwig', 'Dos programadores se dan cuenta de que su amor es el único caso de la clase.', '["Saoirse Ronan", "Timothée Chalamet"]', 'https://www.youtube.com/results?search_query=unique+love+story+movie+trailer', 'Columbia Pictures', 'Inglés', 1),

-- 8. DOCUMENTAL (ID 8): 3 películas
('Bitácora de un Bug', 85, 1, 8, 'Alex Gibney', 'Un seguimiento semana a semana de un *bug* crítico desde su nacimiento hasta su resolución.', '["Linus Torvalds", "Guido van Rossum"]', 'https://www.youtube.com/results?search_query=software+development+documentary+trailer', 'Jigsaw Productions', 'Castellano', 0),
('Crónica del Deployment', 98, 1, 8, 'Werner Herzog', 'La historia real y dramática de un solo despliegue de software.', '["Equipo DevOps"]', 'https://www.youtube.com/results?search_query=it+infrastructure+documentary+trailer', 'BBC Studios', 'Inglés', 1),
('El Espíritu del Copyleft', 112, 1, 8, 'Laura Poitras', 'Un profundo análisis del movimiento de Software Libre y sus implicaciones éticas y sociales.', '["Richard Stallman", "Edward Snowden"]', 'https://www.youtube.com/results?search_query=free+software+movement+documentary+trailer', 'Participant Media', 'Castellano', 0),

-- 9. TERROR (ID 9): 4 películas
('La Venganza del Puntero Nulo', 130, 0, 9, 'James Wan', 'Una pesadilla de programación donde un puntero nulo busca venganza en cada lenguaje.', '["Patrick Wilson", "Vera Farmiga"]', 'https://www.youtube.com/results?search_query=supernatural+tech+horror+trailer', 'New Line Cinema', 'Castellano', 0),
('El Despertar del Legacy', 128, 0, 9, 'Andy Muschietti', 'Un código antiguo y sin documentar cobra vida en la noche.', '["Bill Skarsgård", "Jessica Chastain"]', 'https://www.youtube.com/results?search_query=ancient+code+horror+movie+trailer', 'Warner Bros. Pictures', 'Inglés', 1),
('La Función Recursiva', 112, 0, 9, 'Ari Aster', 'Una función sin condición de parada atormenta a un desarrollador en sus sueños.', '["Toni Collette", "Alex Wolff"]', 'https://www.youtube.com/results?search_query=psychological+horror+loop+trailer', 'A24', 'Castellano', 0),
('Error 418: Soy una tetera', 100, 0, 9, 'Sam Raimi', 'Un *malware* convierte todos los dispositivos IoT en teteras hostiles.', '["Bruce Campbell", "Elizabeth Olsen"]', 'https://www.youtube.com/results?search_query=horror+comedy+iot+teapot+trailer', 'Columbia Pictures', 'Inglés', 1),

-- 10. HISTÓRICAS (ID 10): 3 películas
('Los Foros de la Red', 115, 1, 10, 'David Fincher', 'Un recuento de las primeras comunidades de software libre en internet.', '["Jesse Eisenberg", "Andrew Garfield"]', 'https://www.youtube.com/results?search_query=early+internet+history+movie+trailer', 'Columbia Pictures', 'Castellano', 0),
('El Inicio del Kernel', 150, 1, 10, 'Ron Howard', 'Un drama histórico sobre la creación del primer núcleo monolítico.', '["Russell Crowe", "Jennifer Connelly"]', 'https://www.youtube.com/results?search_query=tech+biography+drama+trailer', 'Imagine Entertainment', 'Inglés', 1),
('Ada: La Primera Programadora', 138, 1, 10, 'Morten Tyldum', 'La biografía de Ada Lovelace y su visión profética de la computación.', '["Keira Knightley", "Benedict Cumberbatch"]', 'https://www.youtube.com/results?search_query=ada+lovelace+biopic+trailer', 'StudioCanal', 'Castellano', 0),

-- 11. CLÁSICO (ID 11): 4 películas
('El Proyecto Pascal (1985)', 140, 1, 11, 'Sydney Pollack', 'Un clásico de culto sobre los inicios de la programación estructurada.', '["Robert Redford", "Dustin Hoffman"]', 'https://www.youtube.com/results?search_query=80s+programming+thriller+trailer', 'Paramount Pictures', 'Inglés', 0),
('El Primer Byte', 95, 1, 11, 'Christopher Nolan', 'La historia de la primera máquina de Turing y su impacto.', '["Cillian Murphy", "Matthew Goode"]', 'https://www.youtube.com/results?search_query=alan+turing+inspired+movie+trailer', 'Syncopy', 'Castellano', 0),
('La Épica de COBOL', 165, 1, 11, 'Ridley Scott', 'Un épico de la década de 1970 sobre la lucha por mantener los sistemas bancarios operativos.', '["Russell Crowe", "Al Pacino"]', 'https://www.youtube.com/results?search_query=banking+system+drama+70s+trailer', '20th Century Studios', 'Inglés', 1),
('Fortran: Los Orígenes', 120, 1, 11, 'Steven Spielberg', 'Una obra maestra en blanco y negro sobre la era de las tarjetas perforadas.', '["Tom Hanks", "Mark Rylance"]', 'https://www.youtube.com/results?search_query=early+computing+history+movie+trailer', 'Amblin Entertainment', 'Castellano', 0),

-- 12. ANIMACIÓN (ID 12): 3 películas
('Aventuras en el Heap', 75, 1, 12, 'Brad Bird', 'Una colorida exploración animada sobre la gestión de memoria.', '["Tom Holland", "Zendaya"]', 'https://www.youtube.com/results?search_query=animated+coding+adventure+trailer', 'Pixar Animation Studios', 'Castellano', 0),
('La Leyenda del Binario', 78, 1, 12, 'Pete Docter', 'Una aventura animada para niños sobre los secretos de los 0s y 1s.', '["Josh Gad", "Kristen Bell"]', 'https://www.youtube.com/results?search_query=animated+numbers+world+movie+trailer', 'Walt Disney Pictures', 'Inglés', 1),
('El Viaje del Paquete TCP', 80, 1, 12, 'Chris Williams', 'Una animación educativa sobre cómo un paquete de datos navega por Internet.', '["Jack Black", "Awkwafina"]', 'https://www.youtube.com/results?search_query=animated+internet+journey+trailer', 'DreamWorks Animation', 'Castellano', 0),

-- 13. AVENTURAS INFORMÁTICAS (ID 13): 3 películas
('La Ruta del Código Perdido', 121, 1, 13, 'Steven Spielberg', 'Un grupo de desarrolladores sigue las pistas dejadas en el código fuente de un viejo servidor para encontrar un algoritmo legendario capaz de optimizar cualquier sistema.', '["Chris Pratt", "Daisy Ridley"]', 'https://www.youtube.com/results?search_query=treasure+hunt+coding+adventure+trailer', 'Amblin Entertainment', 'Castellano', 1),
('Expedición al Data Center Secreto', 129, 1, 13, 'Joss Whedon', 'Un equipo de ingenieros de sistemas se adentra en un gigantesco data center subterráneo donde cada sala es un nuevo reto de redes, seguridad y alta disponibilidad.', '["Robert Downey Jr.", "Scarlett Johansson"]', 'https://www.youtube.com/results?search_query=secret+facility+tech+movie+trailer', 'Marvel Studios', 'Castellano', 0),
('El Tesoro del Repositorio Git', 110, 1, 13, 'Christopher McQuarrie', 'Un joven programador descubre un antiguo repositorio Git lleno de commits encriptados que conducen a un secreto capaz de cambiar el futuro del software libre.', '["Tom Cruise", "Rebecca Ferguson"]', 'https://www.youtube.com/results?search_query=heist+movie+tech+repository+trailer', 'Skydance Media', 'Inglés', 1);

