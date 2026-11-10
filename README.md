# tennis-career

A Python package that retrieves a tennis player's career matches from
[Tennis Abstract](https://www.tennisabstract.com) and plots them in the style of
the New York Times visualization of Serena Williams's career: the player's age
against the age difference with each opponent, colored by win or loss.

## Installation

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-2-agheadley32.git
```

Dependencies (`pandas`, `requests`, `matplotlib`) are installed automatically.

## Usage

```python
from tennis_career import get_career_matches, plot_career_matches

serena = get_career_matches("serena williams")
fig = plot_career_matches(serena)

rafa = get_career_matches("Rafael Nadal")
fig = plot_career_matches(rafa)
fig.savefig("nadal.png")
```

Names are accepted as `"serena williams"`, `"Serena Williams"`, or `"SerenaWilliams"`.
An unknown name raises a `ValueError`:

```python
get_career_matches("GastonSanchez")
# ValueError: Player 'GastonSanchez' not found on Tennis Abstract. ...
```

## Functions

**`get_career_matches(player_name)`** downloads the player's career file and player
page from Tennis Abstract and returns a data frame with one row per match:
`player`, `date`, `result` (`"win"`/`"loss"`), `opponent`, `player_age`,
`opponent_age`, and `age_diff` (player's age minus opponent's age, in years).
Women's career files list each opponent's date of birth, so ages are derived from it;
men's files list the opponent's age directly.

**`plot_career_matches(matches)`** takes that data frame and returns a matplotlib
figure: player's age on the x-axis, age difference on the y-axis, points colored
by result.

## Notes on the data

- Each call makes two requests to Tennis Abstract (career matches and player page,
  for the player's date of birth). If the site is rate-limiting requests, a
  `RuntimeError` asks you to wait and try again.
- Some career files on Tennis Abstract stop before the end of a player's career
  (for example, Rafael Nadal's ends in 2016).
- Matches where the opponent's age is unknown are dropped.

## Running the tests

```bash
pip install -e .
pip install pytest
pytest
```

The tests use mock career files in `tests/fixtures/` and fake HTTP responses,
so they never contact Tennis Abstract.

## Personal reflections

1. Test Passed But The Real Data Broke
- All of my tests passed on the mockup files, but get_career_matches("Rafael Nadal") failed with “No match data found.” The mockups ended with ]], while the real files end with ], a line break, spaces, then ];. The regex only matched the mockup style. I fixed this with \s* and added a test for the real-file ending.

2. Turning HW2 Code Into a Package
- My HW2 code was three scripts that ran top to bottom for one player. They had Serena’s birthdate typed in (1981-09-26), a hard-coded URL, and saved CSV and PNG files. In HW3 that became one data function and one plot function, plus five private helpers, each doing one job.

3. Testing Without Touching The Internet
- The assignment banned live server calls in tests. You used fixture files for parsing and monkeypatch with a FakeResponse class to fake 200, 404, 429 and 500 responses

4. The Litmus Test Caught a Rate Limit
- Installing from GitHub into a fresh environment worked for Serena, Nadal and Federer, then Venus hit 429 Too Many Requests because each player takes two requests. To combat this, I added a clear RuntimeError message for it.

5. Git Workflow
- I made around 20 small commits, each one helper and its test, a fix, or a notebook update, instead of one big upload. This is something I tried to improve upon from feedback on past work.