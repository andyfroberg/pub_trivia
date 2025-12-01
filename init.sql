PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    email TEXT UNIQUE NOT NULL,  -- Needs frontend &/or backend validation
    hashed_mfa_code TEXT,
    hashed_mfa_code_expires_at DATETIME,
    session_id TEXT,
    session_refreshed_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Rounds (
    round_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    difficulty TEXT NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
    question_text TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)  -- CASCADES? Check all FK references
);

CREATE TABLE IF NOT EXISTS Answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    answer_text TEXT NOT NULL,
    is_correct INTEGER NOT NULL CHECK (is_correct IN (0, 1)),  -- SQLite doesn't support boolean: 0=false, 1=true
    question_id INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);

CREATE TABLE IF NOT EXISTS RoundQuestions (
    round_question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    question_id INTEGER NOT NULL,
    round_id INTEGER NOT NULL,
    UNIQUE(question_id, round_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id),
    FOREIGN KEY (round_id) REFERENCES Rounds(round_id)
);

CREATE TABLE IF NOT EXISTS UserAnswers (
    user_answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    answered_correctly INTEGER NOT NULL CHECK (answered_correctly IN (0, 1)),  -- SQLite doesn't support boolean: 0=false, 1=true
    question_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    UNIQUE(question_id, user_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- -- Triggers to auto-update updated_at timestamps (more efficient with WHEN clause)
-- CREATE TRIGGER IF NOT EXISTS update_rounds_timestamp
-- AFTER UPDATE ON Rounds
-- FOR EACH ROW
-- WHEN NEW.updated_at = OLD.updated_at  -- Only trigger if updated_at wasn't manually set
-- BEGIN
--     UPDATE Rounds SET updated_at = CURRENT_TIMESTAMP WHERE round_id = NEW.round_id;
-- END;

-- CREATE TRIGGER IF NOT EXISTS update_questions_timestamp
-- AFTER UPDATE ON Questions
-- FOR EACH ROW
-- WHEN NEW.updated_at = OLD.updated_at
-- BEGIN
--     UPDATE Questions SET updated_at = CURRENT_TIMESTAMP WHERE question_id = NEW.question_id;
-- END;

-- CREATE TRIGGER IF NOT EXISTS update_answers_timestamp
-- AFTER UPDATE ON Answers
-- FOR EACH ROW
-- WHEN NEW.updated_at = OLD.updated_at
-- BEGIN
--     UPDATE Answers SET updated_at = CURRENT_TIMESTAMP WHERE answer_id = NEW.answer_id;
-- END;

-- CREATE TRIGGER IF NOT EXISTS update_round_questions_timestamp
-- AFTER UPDATE ON RoundQuestions
-- FOR EACH ROW
-- WHEN NEW.updated_at = OLD.updated_at
-- BEGIN
--     UPDATE RoundQuestions SET updated_at = CURRENT_TIMESTAMP WHERE round_question_id = NEW.round_question_id;
-- END;

-- CREATE TRIGGER IF NOT EXISTS update_user_answers_timestamp
-- AFTER UPDATE ON UserAnswers
-- FOR EACH ROW
-- WHEN NEW.updated_at = OLD.updated_at
-- BEGIN
--     UPDATE UserAnswers SET updated_at = CURRENT_TIMESTAMP WHERE user_answer_id = NEW.user_answer_id;
-- END;