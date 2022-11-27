-- Keep a log of any SQL queries you execute as you solve the mystery.

/* What We Know:
    1. Humphrey Street Bakery, 10:15 AM
    2. July 28, 2021

   What We Are Solving For:
    1. Thief
    2. Accomplice
    3. Where they escaped to

Using the given */

SELECT description
FROM crime_scene_reports
WHERE month = 7 AND day = 28 AND YEAR = 2021
AND street LIKE "Humphrey Street";

-- Crime took place at 10:15 AM, three witnesses.

SELECT transcript
FROM interviews
WHERE month = 7 AND day = 28 AND YEAR = 2021;

/* Witnesses points to:
    1. Emma's bakery, ealier, withdrawing money from ATM, Leggett Street
    2. Earliest flight out of Fiftyville on the next day, which is the 29th, call less than a minute
    3. Parking lot security footage

From the second clue, we can check the flight logs and solve where the thief escaped to. */

SELECT airports.city
FROM airports
WHERE airports.id =
    (SELECT destination_airport_id
    FROM flights
    WHERE month = 7 AND day = 29 AND year = 2021
    ORDER BY hour ASC, minute ASC)
    LIMIT 1;

-- Earliest flight that day is to NYC
-- Checking ATM on Leggett Street, and possible suspects

SELECT people.name, people.phone_number
FROM people
WHERE people.id IN
    (SELECT bank_accounts.person_id
    FROM bank_accounts
    WHERE bank_accounts.account_number IN
        (SELECT DISTINCT atm_transactions.account_number
        FROM atm_transactions
        WHERE month = 7 AND day = 28 AND year = 2021
        AND atm_location = "Leggett Street"
        AND transaction_type LIKE "withdraw"));

/* Possible suspects:

| Kenny   | (826) 555-1652 |
| Iman    | (829) 555-5269 |
| Benista | (338) 555-6650 |
| Taylor  | (286) 555-6063 |
| Brooke  | (122) 555-4581 |
| Luca    | (389) 555-5198 |
| Diana   | (770) 555-1861 |
| Bruce   | (367) 555-5533 |

Check Bakery logs to see any matches */

SELECT people.name, people.phone_number
FROM people
WHERE people.license_plate IN
    (SELECT license_plate
    FROM bakery_security_logs
    WHERE month = 7 AND day = 28 AND year = 2021
    AND hour = 10 AND minute < 25
    AND activity = "exit");

/* Possible Suspects:
| Vanessa | (725) 555-4692 |
| Barry   | (301) 555-4174 |
| Iman    | (829) 555-5269 | maybe
| Sofia   | (130) 555-0289 |
| Luca    | (389) 555-5198 | maybe
| Diana   | (770) 555-1861 | maybe
| Kelsey  | (499) 555-9472 |
| Bruce   | (367) 555-5533 | maybe

-- Check for calls at this time, to narrow the suspect pool */


SELECT phone_calls.caller
FROM phone_calls
WHERE phone_calls.caller IN ("(829) 555-5269", "(389) 555-5198", "(770) 555-1861", "(367) 555-5533") AND month = 7 AND day = 28 AND year = 2021;

/* Two people from the list of suspects called during this time\, Bruce and Diana, now just check their passport numbers against passengers on the flight to NY */

SELECT people.passport_number, people.name
FROM people
WHERE people.phone_number IN ("(367) 555-5533", "(770) 555-1861");

-- PASSPORT NUMBERS
-- | 3592750733      | Diana |
-- | 5773159633      | Bruce |

SELECT flights.id
FROM flights
WHERE flights.month = 7 AND flights.day = 29
ORDER BY flights.hour ASC, flights.minute ASC
LIMIT 1;

-- Flight ID = 36

SELECT passengers.passport_number
FROM passengers
WHERE passengers.flight_id = 36
AND passengers.passport_number IN (3592750733, 5773159633);

-- Returns passport number: 5773159633. Same as Bruce's. Thief is Bruce.

-- Whoever Bruce was calling when leaving the shop was the accomplice, and the call was less than a minute.


SELECT people.name
FROM people
WHERE people.phone_number IN
(SELECT receiver
FROM phone_calls
WHERE caller = "(367) 555-5533"
AND month = 7
AND day = 28
AND year = 2021
AND duration < 60);

-- Robin was the only one on the call with Bruce for less than a minute, and on the same day he commited the crime.

/* The thief is Bruce, the accomplice is Robin, and the flight destination is NYC. 
