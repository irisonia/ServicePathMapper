# ServicePathMapper

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/downloads/release/python-3100/)
[![GitHub last commit](https://img.shields.io/github/last-commit/irisonia/ServicePathMapper)](https://github.com/irisonia/ServicePathMapper)
[![codecov](https://codecov.io/gh/irisonia/ServicePathMapper/branch/main/graph/badge.svg)](https://codecov.io/gh/irisonia/ServicePathMapper)
[![Made with love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red)](https://github.com/irisonia) by [irisonia](https://github.com/irisonia)

**A Python tool to map and analyze service-based paths between servers in distributed systems, honoring flexible policy constraints.**

---

## Table of Contents

- [Use Cases](#use-cases)
- [Installation](#installation)
- [Usage](#usage)
  - [Minimal Run Example](#minimal-run-example)
- [Input & Output](#input--output)
- [Testing](#testing)
- [Developer Notes](#developer-notes)
  - [CodeBehaviorError](#codebehaviorerror)
  - [Community Feedback & Roadmap](#community-feedback--roadmap)
- [Contact](#contact)
- [License](#license)

---

## Use Cases

- **Discover All Service-Based Paths Between Two Servers in a Complex Distributed System:**  
  Results include:
  - All valid paths, detailing the connected servers and the connecting services, 
    grouped by path length and server group.
  - Detailed analysis of server and service participation in the resulting paths.


- **Apply Policy Constraints to Explore What-If Scenarios:**  
  Example uses:
  - *Simulate Outages:*  
    Mark any servers or services as 'forbidden' from participating in paths, and observe impacts such as:
    - Services now lacking providers or clients.
    - Changes in the number of valid paths.
    - Shifts in the participation of other servers and services in paths.
  - *Security Enforcement:*  
    Only allow paths that include specific servers and services, supporting security policy enforcement.


- **Analyze Server-Service Relationships:**  
  Example uses:
  - **Resource Optimization:** Assess potential workload distribution across servers.
  - **Configuration Cleanup:** Identify services with clients but no providers, or providers but no clients.

---

## Installation

1. **Clone the repository:**

```
git clone https://github.com/irisonia/ServicePathMapper
```


2. **Navigate to the project directory** (where "pyproject.toml" is located):

```
cd servicepathmapper
```


3. **Install the requirements and the program in editable mode:**

```
pip3 install -r requirements.txt

pip3 install -e .
```

---

## Usage

1. **Make sure you have the input prepared.** [See the minimal example](#minimal-run-example)


2. **Ensure you are in the project directory (where "pyproject.toml" is located).**


3. **Run the program:**

```
python3 -m servicepathmapper.service_path_mapper --config path/to/your/config.json
```



* For many usage examples, see the `tests` directory.

---

### Minimal Run Example

The most minimal content would include just the source server and destination server, connected by a single service:


1. Have a `clients` dir and a `providers` dir, each containing a file per server, named after the server,  
listing, one per line, the services this server is a client of (clients dir) or a provider of (providers dir).


```
clients/
└── Server1        # file contains: Service1

providers/
└── Server2        # file contains: Service1
```


2. Have a config file, for example:

**config.json**
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


Inside **stats.json** you will find the config stats and the participation counters.

Inside **log.txt** you will find the raw config input and meaningful messages.

---

### Input & Output

- **Input:**

  - Use `--help` or `-h` for input options details.

  - Use `--help-config` for configuration file details.


- **Output:**

  - All paths that abide by the constraints policy, grouped by path lengths and by server groups. 
  
    For details, see `--help-output` and `--help-paths`.

  - Statistical analysis of the system and the resulting paths.
  
    For details, see `--help-output` and `--help-stats`.

  - Configuration summary and log messages are saved in **log.txt**.

---

## Testing

Run all tests using: 

```
pytest
```

---

## Developer Notes

Feedback is welcome!

Before opening a new issue, please check the [open issues](https://github.com/irisonia/ServicePathMapper/issues) 
to see if your topic has already been reported or is being discussed.


### CodeBehaviorError

If the program ever raises a `CodeBehaviorError`, this indicates an internal consistency or logic issue.

**Please open a [GitHub issue](https://github.com/irisonia/ServicePathMapper/issues)** describing the error and the circumstances that led to it.


### Community Feedback & Roadmap

Check out the [open issues](https://github.com/irisonia/ServicePathMapper/issues) for planned enhancements and feature proposals!

**Upvote** the enhancements that would benefit you most.

**Comment** with your use cases, suggestions, or refinements—your feedback helps prioritize development and ensures new features meet real needs.

If you have ideas for new analytics, stats, or features, feel free to open a new issue or join the discussion.

If you encounter a bug, please open a new issue or join the discussion on existing ones.

Your engagement directly shapes the future of this project!

**Note:** Pull requests are not being accepted at this time.

---

## Contact

For questions, suggestions, or support, please [open an issue](https://github.com/irisonia/ServicePathMapper/issues) or contact [irisonia](https://github.com/irisonia) directly on GitHub.

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

I truly hope you benefit from this project! Sincerely, Irisonia