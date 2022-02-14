#!/usr/bin/env swipl
:- module(server,
      [ server/1            % ?Port
      ]).

:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_files)).
:- use_module(library(http/http_unix_daemon)).
:- use_module(library(http/http_dyn_workers)).
:- use_module(library(http/http_parameters)).

:- [predicats].
:- http_handler(root(.), ping, []).
:- http_handler('/eccn', main(Method), [method(Method), methods([get, put, delete])]).

server(Port) :-
    http_server(http_dispatch, [ port(Port),workers(16)]).

ping(_Request) :-
    format('Content-type: text/plain~n~n'),
    format('OK.').

main(get, Request) :-
    http_parameters(Request, [ score(Score), license(License) ], [attribute_declarations(http_param)]),
    debug(getter, 'GET Request made with: ', [Score, License]),
    format('Content-type: text/plain~n~n'),
    launch_research(Score, License, X),
    format(X).

% TODO <- search for the way to create and setup a new data
main(put, Request) :-
    http_parameters(Request, [ score(_Score), license(_License), code(_Code) ], [attribute_declarations(http_param)]).

main(delete, Request) :-
    http_parameters(Request, [ score(_Score), license(_License)], [attribute_declaration(http_param)]).


http_param(score, [integer, description('Cryptography score.')]).
http_param(license, [string, description('License type.')]).
http_param(code, [string, description('Code ECCN')]).
