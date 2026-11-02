---
tags: [skill-creator]
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent, WebFetch, WebSearch]
---

у нас телеграм бот для записи в барбершоп (aiogram 3, postgres). сейчас если клиент хочет перенести запись он пишет администратору в личку и тот вручную переносит. хочу чтобы клиент сам мог перенести через бота. записи в таблице appointments: id, client_tg_id, master_id, starts_at (timestamptz), duration_min, status. у мастеров расписание в таблице schedule_slots. накидай как это должно работать и как реализовать
