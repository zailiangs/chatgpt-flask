# chatgpt-flask

<a href="https://zailiangs.com" target="_blank" >
<img src="https://img.shields.io/badge/DevelopedBy-Sun Zailiang-blue.svg?" alt=""/>
</a>

> This project is Python access `OpenAI GPT-3.5` model, simple and easy to use, can be used to quickly build chatbots.  
> The response is a `RESTful` protocol, does not contain pages, and uses the `SSE` protocol.  
> What is SSE ? [Server-Sent Events course](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format) &
> [Example Python code](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb)  
> The API of GPT-3.5 is used in the project. You need to apply for an API Key.  
> Apply Links: [OpenAI](https://chat.openai.com)

### Requirements:

- Python 3.8+
- GPT-3.5 API Key
- MySQL 5.7
- Gunicorn

### Configuration:

1. Open the `config.py` file and modify `OPENAI_API_KEY` to your API Key.
2. The sql file is in the `sql` directory, import it into the database.
3. The data source and port number configuration are in the `app.py` file, modify it to your database configuration and
   port number.

### Use:

```shell
# Install dependencies
pip install -r requirements.txt
# Run
gunicorn app:app --bind
```