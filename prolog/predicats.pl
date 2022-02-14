#!/usr/bin/env swipl

license_is("MIT", libre).
license_is("MIT-0", libre).
license_is("MIT-advertising", libre).
license_is("MIT-CMU", libre).
license_is("MIT-CMU", libre).
license_is("Apache-2.0", libre).
license_is("WTFPL", libre).
license_is("BSD-2-Clause", libre).
license_is("Ruby", libre).

is_define(800, public, 'EAR99').
is_define(800, libre, 'EAR99').
is_define(800, fermee, '5D992.c').
is_define(30000, _, 'Manual verification required').
is_define(inf, public, '5D002 - NLR').
is_define(inf, libre, '5D002 - NLR sous réserve de notification du BIS').
is_define(inf, fermee, '5D002').

find_def(_, L, [], X) :- is_define(inf, L, X).
find_def(S, L, [M|R], X) :- (M > S -> is_define(M, L, X) ; find_def(S, L, R, X)).

launch_research(S, L, X) :- (license_is(L, T) -> find_def(S, T, [800, 30000], X) ; find_def(S, fermee, [800, 30000], X)).
