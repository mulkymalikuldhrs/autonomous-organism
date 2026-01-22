import sqlite3 from 'sqlite3';
import path from 'path';

const dbPath = path.resolve(__dirname, 'problems.db');
let db: sqlite3.Database;

interface RawProblem {
  source: string;
  text: string;
}

interface CleanProblem {
    raw_id: number;
    text_clean: string;
}


/**
 * Initializes the SQLite database and creates tables if they don't exist.
 */
export function initializeDatabase(): Promise<void> {
  return new Promise((resolve, reject) => {
    db = new sqlite3.Database(dbPath, (err) => {
      if (err) {
        console.error('Error opening database:', err.message);
        reject(err);
      } else {
        console.log('Connected to the SQLite database.');
        db.serialize(() => {
          db.run(`CREATE TABLE IF NOT EXISTS problem_raw (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            text TEXT NOT NULL,
            date TEXT NOT NULL
          )`, (err) => {
            if (err) {
              console.error('Error creating problem_raw table:', err.message);
              reject(err);
            }
          });

          db.run(`CREATE TABLE IF NOT EXISTS problem_clean (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_id INTEGER,
            text_clean TEXT NOT NULL,
            FOREIGN KEY (raw_id) REFERENCES problem_raw(id)
          )`, (err) => {
            if (err) {
              console.error('Error creating problem_clean table:', err.message);
              reject(err);
            } else {
              resolve();
            }
          });
        });
      }
    });
  });
}

/**
 * Saves an array of raw problems to the 'problem_raw' table.
 *
 * @param problems The array of raw problem objects to save.
 * @returns A promise that resolves with the IDs of the inserted rows.
 */
export function saveRawProblems(problems: RawProblem[]): Promise<number[]> {
  return new Promise((resolve, reject) => {
    if (!db) {
      const err = new Error('Database not initialized. Call initializeDatabase() first.');
      console.error(err.message);
      return reject(err);
    }

    const stmt = db.prepare(`INSERT INTO problem_raw (source, text, date) VALUES (?, ?, ?)`);
    const date = new Date().toISOString();
    const insertedIds: number[] = [];

    db.serialize(() => {
        let completed = 0;
        for (const problem of problems) {
            stmt.run(problem.source, problem.text, date, function(err) {
                if (err) {
                    console.error('Error saving to problem_raw:', err.message);
                    return reject(err);
                }
                insertedIds.push(this.lastID);
                completed++;
                if (completed === problems.length) {
                    stmt.finalize((err) => {
                        if (err) {
                          console.error(`Error finalizing statement for problem_raw:`, err.message);
                          reject(err);
                        } else {
                          console.log(`${problems.length} problems saved to problem_raw.`);
                          resolve(insertedIds);
                        }
                    });
                }
            });
        }
    });
  });
}


/**
 * Saves an array of cleaned problems to the 'problem_clean' table.
 *
 * @param problems The array of clean problem objects to save.
 * @returns A promise that resolves when the operation is complete.
 */
export function saveCleanProblems(problems: CleanProblem[]): Promise<void> {
  return new Promise((resolve, reject) => {
    if (!db) {
      const err = new Error('Database not initialized. Call initializeDatabase() first.');
      console.error(err.message);
      return reject(err);
    }

    const stmt = db.prepare(`INSERT INTO problem_clean (raw_id, text_clean) VALUES (?, ?)`);

    db.serialize(() => {
      for (const problem of problems) {
        stmt.run(problem.raw_id, problem.text_clean);
      }
      stmt.finalize((err) => {
        if (err) {
          console.error(`Error saving to problem_clean:`, err.message);
          reject(err);
        } else {
          console.log(`${problems.length} problems saved to problem_clean.`);
          resolve();
        }
      });
    });
  });
}


/**
 * Closes the database connection.
 */
export function closeDatabase(): Promise<void> {
    return new Promise((resolve, reject) => {
        if (db) {
            db.close((err) => {
                if (err) {
                    console.error('Error closing database:', err.message);
                    return reject(err);
                }
                console.log('Database connection closed.');
                resolve();
            });
        } else {
            resolve(); // No db to close
        }
    });
}
