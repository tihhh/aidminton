DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS injury_logs;
DROP TABLE IF EXISTS common_injuries;
DROP TABLE IF EXISTS medical_experts;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nickname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE injury_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    date TEXT NOT NULL,
    pain_level INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE common_injuries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    symptoms TEXT NOT NULL,
    treatment TEXT NOT NULL,
    prevention TEXT NOT NULL,
    image_path TEXT
);

CREATE TABLE medical_experts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    hospital TEXT NOT NULL,
    contact TEXT NOT NULL,
    image_path TEXT
);

-- Insert some sample data for common injuries
INSERT INTO common_injuries (title, description, symptoms, treatment, prevention, image_path)
VALUES 
    ('Ankle Sprain', 'An injury that occurs when you roll, twist or turn your ankle in an awkward way.', 'Pain, swelling, bruising, limited range of motion', 'Rest, ice, compression, elevation (RICE)', 'Proper warm-up, supportive footwear, strength training', '/static/images/ankle_sprain.jpg'),
    ('Tennis Elbow', 'Inflammation of the tendons that join the forearm muscles to the outside of the elbow.', 'Pain and tenderness on the outside of the elbow', 'Rest, physical therapy, anti-inflammatory medication', 'Proper technique, equipment sizing, strengthening exercises', '/static/images/tennis_elbow.jpg'),
    ('Knee Strain', 'Stretched or torn ligaments, tendons, or muscles that support the knee.', 'Pain, swelling, stiffness, weakness', 'RICE protocol, bracing, physical therapy', 'Proper warm-up, technique, and training progression', '/static/images/knee_strain.jpg');

-- Insert sample medical experts
INSERT INTO medical_experts (name, specialty, hospital, contact, image_path)
VALUES
    ('Dr. MEI', 'General Practitioner', 'RS Moth', '+628123456789', '/static/images/doctor1.png'),
    ('House, MD', 'Orthopedic Surgery', 'Princeton Plainsboro Teaching Hospital', '+1-555-345-6789', '/static/images/doctor2.jpg'),
    ('Dr. Shaun Murphy', 'Physical Therapy', 'San Jose St. Bonaventure Hospital', '+1-333-333-3333', '/static/images/doctor3.png');
