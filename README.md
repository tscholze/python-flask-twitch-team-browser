# Twitch Teams Browser
> A simple Python Flask web app that helps to browse Twtich team member by unsing the API team data.

## Status

|Type|Status|
|----|------|
|Build (Travis)| - |

## Requirements

- Python 3.6.3
- `pip install flask requests`
- Twitch API client id ([Developer Dashboard](https://dev.twitch.tv/console/apps))

## Configuration

Open `main.py` and fill in the required `TWITCH_CLIENT_ID` constant with Twitch API client id.
To change the templates, have a look at the folder `templates/`.

## Run

```
> python python-flask-twitch-team-browser/main.py
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```

![Screenshot](https://tscholze.uber.space/wp-content/uploads/2019/04/Bildschirmfoto-2019-04-06-um-09.08.08-768x937.png)

## Publications
- Personal Blog: [[Python & Flask] Twitch Teams Browser](https://tscholze.uber.space/2019/04/06/python-flask-twitch-teams-browser/)


## Contributing

Feel free to improve the quality of the code. It would be great to learn more from experienced Python developers.

## Authors

Just me, [Tobi]([https://tscholze.github.io).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
Dependencies or assets maybe licensed differently.
