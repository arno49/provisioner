# Ansible wrapper
Ansible wrapper for provisionning automation.

## How to use


Use ./run to operate.


* Developing

```bash
~ localhost >> vagrant up
~ localhost >> vagrant ssh
~ vagrant >> ./run -p playbooks/base/bake-nginx.yml
```

* Forking

TBD

* Structure
```text

.
├── LICENSE
├── README.md
├── Vagrantfile
├── ansible.cfg
├── bin                         # custom tools
│   └── parser.py
├── galaxy-roles                # galaxy dependencies
│   └── README.md
├── library                     # custom library
│   ├── aws_lambda_call
│   ├── clean_logs
│   ├── s33
│   └── structure_unpack
├── playbooks
│   └── base                    # related playbooks 
│       ├── bake-nginx.yml
│       └── requirements.yml    # playbooks requirements
├── requirements
├── roles                       # custom roles
│   └── README.md
└── run
```