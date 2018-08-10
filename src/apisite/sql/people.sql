
create table companys (
    company_id INT NOT NULL AUTO_INCREMENT,
    company_name TEXT(100) NOT NULL,
    PRIMARY KEY (company_id)
);

create table users (
    user_id INT NOT NULL AUTO_INCREMENT,
    user_name TEXT(40) NOT NULL,
    password VARCHAR(100) NOT NULL,
    status INT NOT NULL DEFAULT 1,
    company_id INT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companys (company_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id)
);


CREATE INDEX company_user ON users(company_id);

create table to_verify(
    verifier INT NOT NULL,
    verifiee INT NOT NULL,
    FOREIGN KEY (verifier) REFERENCES users (user_id) ON DELETE CASCADE,
    FOREIGN KEY (verifiee) REFERENCES users (user_id) ON DELETE CASCADE,
    PRIMARY KEY (verifier, verifiee)
);

CREATE INDEX verifier_index ON to_verify(verifier);
CREATE INDEX verifiee_index ON to_verify(verifiee);

create table cooperation(
    cooperation_id INT NOT NULL AUTO_INCREMENT,
	user_id INT NOT NULL,
	company_id INT NOT NULL,
	duration INT NOT NULL DEFAULT 1,
	project TEXT(200),
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
	FOREIGN KEY (company_id) REFERENCES companys (company_id) ON DELETE CASCADE,
	PRIMARY KEY (cooperation_id)
);