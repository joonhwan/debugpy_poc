# debugpy POC

## step 1. debug server / adapter 를 통하여 debuggee 실행 

아래 명령은 `pydebuggee` 모듈의 `__main__.py` 를 실행하는 debug adapter(내부적으로 server도 실행)하고, 56789 포트를 열고 접속을 대기하게 한다. 

```
> python -m debugpy --wait-for-client  --listen 56789 -m pydebuggee 
```

## step 2. 간이 command line 구현된 debugger 를 실행. 

실행후, recv 가 없을때까지 대기하였다가, 커서가 떨어지면, 

- `init` : 초기화하고, 중단점을 설정한다.
- `done` : 설정이 완료되었음을 알려, debuggee 가 실행되도록 한다.  중단점 설정된 곳까지 쭉 실행된다.
- `st` : 현재 stack trace를 확인.
- `scopes` : 현재 접근 가능 scopes 를 확인.
- `var` : 특정 varaible reference에 대한 변수 정보를 확인
- `n` : next 
- `c`  : continue

의 간이 명령어들을 순서대로 입력하여 볼 수 있다. 

```
> python attach_debuggee.py
len =  1
using port :  56789
connected!
response : 
{
  "seq": 1,
  "type": "event",
  "event": "output",
  "body": {
    "category": "telemetry",
    "output": "ptvsd",
    "data": {
      "packageVersion": "1.4.1"
    }
  }
}

response : 
{
  "seq": 2,
  "type": "event",
  "event": "output",
  "body": {
    "category": "telemetry",
    "output": "debugpy",
    "data": {
      "packageVersion": "1.4.1"
    }
  }
}

response : 
[
  {
    "seq": 1,
    "type": "event",
    "event": "output",
    "body": {
      "category": "telemetry",
      "output": "ptvsd",
      "data": {
        "packageVersion": "1.4.1"
      }
    }
  },
  {
    "seq": 2,
    "type": "event",
    "event": "output",
    "body": {
      "category": "telemetry",
      "output": "debugpy",
      "data": {
        "packageVersion": "1.4.1"
      }
    }
  }
]
```

위와 같이 나오면, `init`

```
init
---------------------------
sending :  initialize
Content-Length: 176

{
  "seq": 4,
  "type": "request",
  "command": "initialize",
  "arguments": {
    "clientID": "rcid",
    "clientName": "recipe_creator_name",
    "adapterID": "debugpy"
  }
}

response : 
{
  "seq": 3,
  "type": "response",
  "request_seq": 4,
  "success": true,
  "command": "initialize",
  "body": {
    "supportsCompletionsRequest": true,
    "supportsConditionalBreakpoints": true,
    "supportsConfigurationDoneRequest": true,
    "supportsDebuggerProperties": true,
    "supportsDelayedStackTraceLoading": true,
    "supportsEvaluateForHovers": true,
    "supportsExceptionInfoRequest": true,
    "supportsExceptionOptions": true,
    "supportsFunctionBreakpoints": true,
    "supportsHitConditionalBreakpoints": true,
    "supportsLogPoints": true,
    "supportsModulesRequest": true,
    "supportsSetExpression": true,
    "supportsSetVariable": true,
    "supportsValueFormattingOptions": true,
    "supportsTerminateDebuggee": true,
    "supportsGotoTargetsRequest": true,
    "supportsClipboardContext": true,
    "exceptionBreakpointFilters": [
      {
        "filter": "raised",
        "label": "Raised Exceptions",
        "default": false
      },
      {
        "filter": "uncaught",
        "label": "Uncaught Exceptions",
        "default": true
      }
    ],
    "supportsStepInTargetsRequest": true
  }
}

---------------------------
sending :  attach
Content-Length: 102

{
  "seq": 6,
  "type": "request",
  "command": "attach",
  "arguments": {
    "__restart": null
  }
}

response : 
{
  "seq": 4,
  "type": "event",
  "event": "debugpyWaitingForServer",
  "body": {
    "host": "127.0.0.1",
    "port": 51029
  }
}

response : 
{
  "seq": 5,
  "type": "event",
  "event": "initialized"
}

---------------------------
sending :  setBreakpoints
Content-Length: 271

{
  "seq": 9,
  "type": "request",
  "command": "setBreakpoints",
  "arguments": {
    "source": {
      "path": "/Users/vine/prj/py-debug/csharp-debugpy/test-py-debugee/pydebuggee/api/__init__.py"
    },
    "breakpoints": [
      {
        "line": 2
      }
    ]
  }
}

response : 
{
  "seq": 6,
  "type": "response",
  "request_seq": 9,
  "success": true,
  "command": "setBreakpoints",
  "body": {
    "breakpoints": [
      {
        "verified": true,
        "id": 0,
        "source": {
          "path": "/Users/vine/prj/py-debug/csharp-debugpy/test-py-debugee/pydebuggee/api/__init__.py"
        },
        "line": 2
      }
    ]
  }
}
```

여기까지 나오면 `done` 을 입력하고 엔터.

```
done
---------------------------
sending :  configurationDone
Content-Length: 89

{
  "seq": 11,
  "type": "request",
  "command": "configurationDone",
  "arguments": {}
}

response : 
{
  "seq": 7,
  "type": "response",
  "request_seq": 11,
  "success": true,
  "command": "configurationDone"
}

response : 
{
  "seq": 8,
  "type": "response",
  "request_seq": 6,
  "success": true,
  "command": "attach"
}

response : 
{
  "seq": 9,
  "type": "event",
  "event": "process",
  "body": {
    "name": "/Users/vine/prj/py-debug/csharp-debugpy/test-py-debugee/pydebuggee/__init__.py",
    "systemProcessId": 3568,
    "isLocalProcess": true,
    "startMethod": "attach"
  }
}

response : 
{
  "seq": 10,
  "type": "event",
  "event": "thread",
  "body": {
    "reason": "started",
    "threadId": 1
  }
}

response : 
{
  "seq": 11,
  "type": "event",
  "event": "stopped",
  "body": {
    "reason": "breakpoint",
    "threadId": 1,
    "preserveFocusHint": false,
    "allThreadsStopped": true
  }
}
```

이제 stack trace를 보기위해 `st` 를 입력하고 엔터.

```
st
---------------------------
sending :  stackTrace
Content-Length: 103

{
  "seq": 17,
  "type": "request",
  "command": "stackTrace",
  "arguments": {
    "threadId": 1
  }
}

response : 
{
  "seq": 12,
  "type": "response",
  "request_seq": 17,
  "success": true,
  "command": "stackTrace",
  "body": {
    "stackFrames": [
      {
        "id": 2,
        "name": "greet",
        "line": 2,
        "column": 1,
        "source": {
          "path": "/Users/vine/prj/py-debug/csharp-debugpy/test-py-debugee/pydebuggee/api/__init__.py",
          "sourceReference": 0
        }
      },
      {
        "id": 3,
        "name": "main",
        "line": 5,
        "column": 1,
        "source": {
          "path": "/Users/vine/prj/py-debug/csharp-debugpy/test-py-debugee/pydebuggee/__main__.py",
          "sourceReference": 0
        }
      },
      {
        "id": 4,
        "name": "<module>",
        "line": 9,
        "column": 1,
        "source": {
          "path": "/Users/vine/prj/py-debug/csharp-debugpy/test-py-debugee/pydebuggee/__main__.py",
          "sourceReference": 0
        }
      }
    ],
    "totalFrames": 3
  }
}

response : 
{
  "seq": 13,
  "type": "event",
  "event": "module",
  "body": {
    "reason": "new",
    "module": {
      "id": 0,
      "name": "pydebuggee.api",
      "path": "/Users/vine/prj/py-debug/csharp-debugpy/test-py-debugee/pydebuggee/api/__init__.py",
      "package": "pydebuggee.api"
    }
  }
}

response : 
{
  "seq": 14,
  "type": "event",
  "event": "module",
  "body": {
    "reason": "new",
    "module": {
      "id": 1,
      "name": "__main__",
      "path": "/Users/vine/prj/py-debug/csharp-debugpy/test-py-debugee/pydebuggee/__main__.py",
      "package": "pydebuggee"
    }
  }
}

response : 
{
  "seq": 15,
  "type": "event",
  "event": "module",
  "body": {
    "reason": "new",
    "module": {
      "id": 2,
      "name": "runpy",
      "path": "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/runpy.py"
    }
  }
}
```

위에서 stack trace 외에 모듈이 불러들여지는 과정이 이벤트로 수신되는 듯 하다. 
이제 현재 접근가능한 scope들(python의 경우, local 및 global)의 id 를 확인하기 위해 
`scopes` 를 입력하고 엔터. 

```
scopes 
---------------------------
sending :  scopes
Content-Length: 98

{
  "seq": 22,
  "type": "request",
  "command": "scopes",
  "arguments": {
    "frameId": 2
  }
}

response : 
{
  "seq": 16,
  "type": "response",
  "request_seq": 22,
  "success": true,
  "command": "scopes",
  "body": {
    "scopes": [
      {
        "name": "Locals",
        "variablesReference": 5,
        "expensive": false,
        "presentationHint": "locals",
        "source": {}
      },
      {
        "name": "Globals",
        "variablesReference": 6,
        "expensive": false,
        "source": {}
      }
    ]
  }
}
```

위에서 local 영역의 scopes 에 대한 referece값(일종의 id?)이 `5` 임을 알았다. 
이제 이걸로 해당 scopes의 모든 변수들에 대한 정보를 가져오기 위해 

`var 5` 라고 입력하고 엔터 


```
var 5
---------------------------
sending :  variables
Content-Length: 112

{
  "seq": 24,
  "type": "request",
  "command": "variables",
  "arguments": {
    "variablesReference": 5
  }
}

response : 
{
  "seq": 17,
  "type": "response",
  "request_seq": 24,
  "success": true,
  "command": "variables",
  "body": {
    "variables": [
      {
        "name": "name",
        "value": "'joonhwan'",
        "type": "str",
        "evaluateName": "name",
        "variablesReference": 0,
        "presentationHint": {
          "attributes": [
            "rawString"
          ]
        }
      },
      {
        "name": "number",
        "value": "10",
        "type": "int",
        "evaluateName": "number",
        "variablesReference": 0
      }
    ]
  }
}
```

한편 global 에는 별게 없다. `var 6` 하고 엔터.
special variables 라는 것과 function variables , 그리고 operation에 대한 variable 정보가 나오는 듯 하다.
아직 학습안됨. protocol 문서를 자세히 봐야 함. 

```
var 6
---------------------------
sending :  variables
Content-Length: 112

{
  "seq": 26,
  "type": "request",
  "command": "variables",
  "arguments": {
    "variablesReference": 6
  }
}

response : 
{
  "seq": 18,
  "type": "response",
  "request_seq": 26,
  "success": true,
  "command": "variables",
  "body": {
    "variables": [
      {
        "name": "special variables",
        "value": "",
        "type": "",
        "evaluateName": "special variables",
        "variablesReference": 7
      },
      {
        "name": "function variables",
        "value": "",
        "type": "",
        "evaluateName": "function variables",
        "variablesReference": 8
      },
      {
        "name": "operation",
        "value": "<module 'pydebuggee.api.operation' from '/Users/vine/prj/py-debug/csharp-debugpy/test-py-debugee/pydebuggee/api/operation.py'>",
        "type": "module",
        "evaluateName": "operation",
        "variablesReference": 9
      }
    ]
  }
}
```

이제 next line을 실행하기 위해 `n` 을 입력하고 엔터. 

```
n
---------------------------
sending :  next
Content-Length: 97

{
  "seq": 28,
  "type": "request",
  "command": "next",
  "arguments": {
    "threadId": 1
  }
}

response : 
{
  "seq": 19,
  "type": "response",
  "request_seq": 28,
  "success": true,
  "command": "next"
}

response : 
{
  "seq": 20,
  "type": "event",
  "event": "continued",
  "body": {
    "threadId": 1,
    "allThreadsContinued": true
  }
}

response : 
{
  "seq": 21,
  "type": "event",
  "event": "stopped",
  "body": {
    "reason": "step",
    "threadId": 1,
    "preserveFocusHint": false,
    "allThreadsStopped": true
  }
}

```

소스코드 라인 번호를 잘 보면 그 다음행이 실행되었음을 알 수 있다. 
끝까지 실행하기 위해 `c`  를 입력하고 엔터. 

```
c
---------------------------
sending :  continue
Content-Length: 101

{
  "seq": 32,
  "type": "request",
  "command": "continue",
  "arguments": {
    "threadId": 1
  }
}

response : 
{
  "seq": 22,
  "type": "response",
  "request_seq": 32,
  "success": true,
  "command": "continue",
  "body": {
    "allThreadsContinued": true
  }
}

response : 
{
  "seq": 23,
  "type": "event",
  "event": "continued",
  "body": {
    "threadId": 1,
    "allThreadsContinued": true
  }
}

response : 
{
  "seq": 24,
  "type": "event",
  "event": "thread",
  "body": {
    "reason": "exited",
    "threadId": 1
  }
}

response : 
{
  "seq": 25,
  "type": "event",
  "event": "terminated"
}
```