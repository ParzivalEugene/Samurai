create table "default".servers
(
    id                serial not null
        constraint servers_pk
            primary key,
    discord_server_id bigint not null
);

create table "default".users
(
    id              serial not null
        constraint users_pk
            primary key,
    discord_user_id bigint not null
);

create table "default".connect
(
    id        bigserial not null,
    server_id bigint    not null
        constraint connect_servers_id_fk
            references "default".servers,
    user_id   bigint    not null
        constraint connect_users_id_fk
            references "default".users
);

create table "default".servers_levels
(
    server_id bigint not null
        constraint servers_levels_servers_id_fk
            references "default".servers,
    level_id  bigint not null,
    level_xp  bigint
);

create table "default".users_levels
(
    server_id bigint not null
        constraint users_levels_servers_id_fk
            references "default".servers,
    user_id   bigint not null
        constraint users_levels_users_id_fk
            references "default".users,
    level     bigint not null,
    xp        bigint not null
);

create table "default".birthdays
(
    user_id bigint not null
        constraint birthdays_users_id_fk
            references "default".users,
    date    date   not null
);

create table "default".servers_chats
(
    server_id          bigint not null
        constraint servers_chats_servers_id_fk
            references "default".servers,
    click_to_role_chat bigint,
    welcome_chat       bigint,
    info_chat          bigint,
    bot_github_chat    bigint,
    join_leave_chat    bigint
);

create table "default".detect_language_game
(
    server_id bigint not null
        constraint detect_language_game_servers_id_fk
            references "default".servers,
    language  text   not null
);

create table "default".connect_four_game
(
    server_id bigint   not null
        constraint connect_four_game_servers_id_fk
            references "default".servers,
    board     bigint[] not null,
    game_over boolean,
    game_type integer  not null,
    turn      bigint
        constraint connect_four_game_users_id_fk
            references "default".users,
    players   bigint[],
    count     integer  not null,
    mark      char,
    pos       integer
);

create table "default".tic_tac_toe_game
(
    server_id bigint    not null
        constraint tic_tac_toe_game_servers_id_fk
            references "default".servers,
    board     integer[] not null,
    game_over boolean   not null,
    game_type integer   not null,
    turn      bigint    not null
        constraint tic_tac_toe_game_users_id_fk
            references "default".users,
    players   bigint[]  not null,
    count     integer   not null,
    mark      char,
    pos       integer   not null
);

create table "default".detect_language_game_statistic
(
    id         serial  not null,
    server_id  bigint  not null
        constraint detect_language_statistic_servers_id_fk
            references "default".servers,
    player     bigint  not null
        constraint detect_language_statistic_users_id_fk
            references "default".users,
    win_status boolean not null,
    language   text    not null
);

create table "default".connect_four_game_statistic
(
    id        serial    not null,
    server_id bigint    not null
        constraint connect_four_game_statistic_servers_id_fk
            references "default".servers,
    game_type integer   not null,
    players   bigint[]  not null,
    winner    bigint    not null
        constraint connect_four_game_statistic_users_id_fk
            references "default".users,
    loser     bigint    not null
        constraint connect_four_game_statistic_users_id_fk_2
            references "default".users,
    board     integer[] not null,
    mark      char      not null,
    count     integer   not null
);

create table "default".tic_tac_toe_game_statistic
(
    id        serial    not null,
    server_id bigint    not null
        constraint tic_tac_toe_game_statistic_servers_id_fk
            references "default".servers,
    game_type integer   not null,
    players   bigint[]  not null,
    winner    bigint    not null
        constraint tic_tac_toe_game_statistic_users_id_fk
            references "default".users,
    loser     bigint    not null
        constraint tic_tac_toe_game_statistic_users_id_fk_2
            references "default".users,
    board     integer[] not null,
    mark      char      not null,
    count     integer   not null
);


