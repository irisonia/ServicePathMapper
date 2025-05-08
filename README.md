# ServicePathMapper

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/downloads/release/python-3100/)
[![GitHub last commit](https://img.shields.io/github/last-commit/irisonia/ServicePathMapper)](https://github.com/irisonia/ServicePathMapper)
[![codecov](https://codecov.io/gh/irisonia/ServicePathMapper/branch/main/graph/badge.svg)](https://codecov.io/gh/irisonia/ServicePathMapper)
[![Made with love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red)](https://github.com/irisonia) by [irisonia](https://github.com/irisonia)

Map and analyze service-based paths between servers in a distributed system, honoring policy constraints.

---

## Features

- Discover all service-based paths between two servers, honoring policy constraints.
- Simulate "what-if" scenarios, such as server/service outages.
- Enforce security policies by requiring or forbidding specific servers/services in paths.
- Analyze and optimize resource allocation and configuration.
- Output detailed statistics about both the system and the resulting paths.

---

## Use Case Examples

- **Path Discovery:**  
  Find all service-based paths between two servers in a distributed system, and analyze the participation of each server and service.

- **What-if Scenarios:**  
  Apply flexible constraints to explore “what-if” scenarios.  
  Example:  
  *Outages Simulation* - List any servers/services as 'forbidden' (not allowed to participate in paths) and observe impacts such as:
    - Changes in the number of valid paths.
    - Shifts in the participation of other servers and services.
    - Services now lacking providers or clients.

- **Security Enforcement:**  
  Force paths to necessarily include designated servers and services, supporting security policy enforcement.

- **Optimize System Resources:**  
    - **Resource Allocation:** Analyze potential workload distribution across servers.
    - **Configuration Cleanup:** Identify services that have clients but no providers, or providers but no clients.

---

## Installation

1. **Clone the repository:**  
`git clone https://github.com/irisonia/ServicePathMapper`


2. **Navigate to the project directory** (where "pyproject.toml" is located):
`cd servicepathmapper`  


3. **Install the requirements and the program in editable mode:**
`pip3 install -r requirements.txt`  
`pip3 install -e .`

---

## Usage

1. Make sure you have the input prepared. [See the minimal example](#minimal-run-example)


2. **Navigate to the project directory** (where "pyproject.toml" is located):  
`cd servicepathmapper`


3. **Run the program:**  
`python3 -m servicepathmapper.service_path_mapper --config path/to/your/config.json`


* For help about the config.json, use `--help-config`.
* For many usage examples, see the `tests` directory.

---

### Minimal Run Example

1. Have a `clients` dir and a `providers` dir, each containing a file per server, named after the server,  
listing, one per line, the services this server is a client of (clients dir) or a provider of (providers dir).
The most minimal content would include just the src-server and dst-server, connected by a single service:

```
clients/
└── Server1        # file contains: Service1

providers/
└── Server2        # file contains: Service1
```

2. Have a config file, for example:  
`config.json`

```json
{
  "clients-dir": "./clients",
  "providers-dir": "./providers",
  "src-server": "Server1",
  "dst-server": "Server2",
  "max-path-len": 5,
  "output-dir": "./my_output_dir"
}
```

3. Run, and observe output. In this minimal example, the output would be:

```
my_output_dir/
├── path_len_2/
│   ├── 0
│   └── 0_servers_group
├── log.txt
└── stats.json
```  

Inside file `0`, you will find a single service-based path:

```
Server1 [Service1] Server2
```

Inside file `0_servers_group`, you will find the participating servers:

```
Server1
Server2
```

In `stats.json` you will find the config stats and the participation counters.  
In `log.txt` you will find the raw config input and meaningful messages.

---

### Input & Output

- Use `--help` or `-h` for detailed input and configuration options.
- **Key outputs:**
  - Paths between servers, with connecting services, grouped by server groups and by path lengths.
  - Statistical analysis of the system and the resulting paths.
- For details, see `--help-output`, `--help-paths`, and `--help-stats`.
- Log messages are saved in `log.txt`.

---

## Testing

- Run all tests using:
`pytest`

---

## Developer Notes

- **CodeBehaviorAlert:**  
If the program ever raises a `CodeBehaviorAlert`, this indicates an internal consistency or logic issue.  
**Please open a GitHub issue** describing the error and the circumstances that led to it.  
Before opening a new issue, check the [open issues](https://github.com/irisonia/ServicePathMapper/issues) to see if it’s already reported or being discussed.  
Feel free to comment, add information, or suggest fixes on existing issues-your feedback is valuable!

- **Contributing & Roadmap:**  
See the [open issues](https://github.com/irisonia/ServicePathMapper/issues) for bugs, feature requests, and planned enhancements.  
If you encounter a bug or have feedback or ideas, please open a new issue or join the discussion on existing ones.
Pull requests are not being accepted at this time.

---

## Coming Soon

- **Detect and Report Unreachable and Dead-End Servers for System Analysis and Runtime Optimization**  
  https://github.com/irisonia/ServicePathMapper/issues/1

- **Allow Splitting Stats Output into Separate Files in a Dedicated Folder**  
  https://github.com/irisonia/ServicePathMapper/issues/2

- **Set an Upper Limit for max-threads Argument**  
  https://github.com/irisonia/ServicePathMapper/issues/3

Feedback is welcome, and I truly hope you benefit from the project!

---

## Contact

For questions, suggestions, or support, please [open an issue](https://github.com/irisonia/ServicePathMapper/issues) or contact [irisonia](https://github.com/irisonia) directly on GitHub.

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
