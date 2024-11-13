


### Sleeper Integration References

#### API Docs
https://docs.sleeper.com/

#### Test Sleeper API Data
League ID: 1049226125907603456

User ID: 1130174389980434432

URL TEST: 
`http://127.0.0.1:8000/api/sleeper/league/1049226125907603456/`


example rulebook request:

```json
{
    "league_id": "1049226125907603456",
    "name": "League of Extraordinary Degenerates Rulebook",
    "description": "Official rulebook for the 2024 season",
    "rules": [
        {
            "rule_title": "Roster Composition",
            "rule_description": "Each team must maintain a specific roster structure.",
            "ordering": 1,
            "subsections": [
                {
                    "subsection_title": "Starting Lineup",
                    "subsection_content": "1 QB, 2 RB, 2 WR, 1 TE, 1 FLEX, 1 K, 1 DEF",
                    "ordering": 1
                },
                {
                    "subsection_title": "Bench Slots",
                    "subsection_content": "5 bench slots available",
                    "ordering": 2
                }
            ]
        },
        {
            "rule_title": "Scoring System",
            "rule_description": "Points are awarded based on player performance.",
            "ordering": 2,
            "subsections": [
                {
                    "subsection_title": "Passing",
                    "subsection_content": "1 point per 25 passing yards, 4 points per passing TD",
                    "ordering": 1
                },
                {
                    "subsection_title": "Rushing",
                    "subsection_content": "1 point per 10 rushing yards, 6 points per rushing TD",
                    "ordering": 2
                }
            ]
        }
    ]
}
```

### Install command 
`pip install -r requirements.txt` should install all the requirements. Need to clean this up

### Jupyter 
jupyter notebook

Create Jupyter Notebook files within the `notebooks` directory for development and testing purposes.
