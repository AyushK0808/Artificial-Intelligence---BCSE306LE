% HTTP Handlers
:- http_handler(root(scholarship), check_scholarship, []).
:- http_handler(root(exam_permission), check_exam_permission, []).

% Start HTTP Server
start_server(Port) :-
    http_server(http_dispatch, [port(Port)]).

% Check scholarship eligibility
check_scholarship(Request) :-
    http_parameters(Request, [student_id(Student_ID, [atom])]),
    (   eligible_for_scholarship(Student_ID)
    ->  Reply = json{status: "eligible"}
    ;   Reply = json{status: "not eligible"}
    ),
    reply_json(Reply).

% Check exam permission
check_exam_permission(Request) :-
    http_parameters(Request, [student_id(Student_ID, [atom])]),
    (   permitted_for_exam(Student_ID)
    ->  Reply = json{status: "permitted"}
    ;   Reply = json{status: "not permitted"}
    ),
    reply_json(Reply).