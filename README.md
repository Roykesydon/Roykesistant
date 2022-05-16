# Introduction
A simple telegram bot with flask.<br/>

Use AES/CFB encrypt message.<br/>

![](./source/demo.png)

# How To Create Your Own Bot

1. Apply to "BotFather" for your bot token

1. write config.yml
    - bot token

    - add your username to whitelist

    - AES key
        - You can use "generate_key.py" to generate your own key

1. write .env
    - DB_USERNAME: root's username
    - DB_PASSWORD: root's password
    


2. ```bat
    docker-compose up -d
    ```

## How to Shut down
```
docker-compose down
```


# Port
- flask : 11539
- mongodb : 27017
- mongo-express : 8081

# API
- `POST` /send

    - Parameters

        name | info
        -- | --
        iv | AES initial vector
        encrypted_message | encrypted < message and timestamp >


# Note 
- If API needs iv and encrypted_message

    you can use
    ```python
    from utils.security_guard import SecurityGuard
    
    security_guard = SecurityGuard()
    iv, encypt_message = security_guard.encrypt_message(<msg>, <key>)
    ```
    to get these parameters
