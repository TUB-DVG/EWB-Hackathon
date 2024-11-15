# ewb-hackathon

This repo contains good-practice, code-snippets and other resources for the Energiewendebauen Hackathon 2024 (ewb-hackathon). The goal of this repo is to provide a starting point for participants to build their projects and give researchers orientation on how to set up their repositories. For this reason, everything in this repo is documented in more detail than is typically the case.As with any example, there are always exceptions and the repo serves as a guide so that it can and must be adapted to the needs of the software project. For example, not every project requires a public folder, as not every project has static content delivery files.  

# Goals of the Hackathon

There are two exemplary questions that the participants will be asked to answer:

1. How can we create a datapipeline, that enables querying data from different CityGML sources?
2. How can we help urban planners identify rooftop areas available for PV installation?

## Project Structure
```bash
hackathon-project/
├── README.md                     # Project overview, setup, usage, and contributions
├── LICENSE                       # License file
├── .gitignore                    # Git ignore file
├── .github/                      # Github specific files
│   ├── CODEOWNERS                # Codeowners file
│   └── CONTRIBUTING.md           # Contributing guidelines
├── docs/
│   ├── setup.md                  # Setup instructions
│   ├── api.md                    # API documentation
│   ├── good-practice.md          # Good Practice for Software Development
│   └── architecture.md           # Architecture overview
├── data/                         # Data files
├── src/
│   ├── client/                   # Frontend code
│   ├── server/                   # Backend code
│   └── components/               # Reusable code components
├── public/
│   ├── index.html                # HTML entry point
│   └── css/                      # CSS files
├── tests/
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── e2e/                      # End-to-end tests
├── config/
│   ├── env.sample                # Example environment variables
│   └── config.json               # Project configuration file
├── assets/                       # Non-code assets like images, fonts, icons
└── scripts/
    ├── deploy.sh                 # Deployment script
    └── setup.sh                  # Environment setup script
```	

## Getting Started

### Prerequisites

We assume [git](https://git-scm.com/), [python](https://www.python.org/) and [docker](https://www.docker.com/) are installed on your machine.

### Installation

As this is a hackathon project, the project structure is not yet fully defined. This will be updated in the future.

1. Clone the repository:
   ```
   git clone https://github.com/username/repo-name.git
   ```
2. Navigate to the project directory:
   ```
   cd repo-name
   ```
3. Install the dependencies / set up the environment:
   ```
   npm install
   ```
4. Set up environment variables by renaming `.env.sample` to `.env` and updating the values.


## Contributing

Beside the two exemplary questions, we also welcome any other ideas for projects that you think would be helpful for the participants. Do you have any good practices, code-snippets or other resources that you think would be helpful for the participants? Please let us know! See the [CONTRIBUTING.md](./github/CONTRIBUTING.md) file for more information on how to contribute to this repo.

## Style Guide

The Style guide for the project can be viewed [here](./styleGuide.md).


## License / Copyright

This repository is licensed under [MIT License](LICENSE).


## Acknowledgements

![Alt text](./assets/logos/BMWK_Logo_2021.svg)

We gratefully acknowledge the financial support by the Federal Ministry for Economic Affairs and Climate Action (BMWK), promotional reference: 03EWB004A.We are grateful for the support by the project [NEED - Neue Daten für die Energiewende](https://www.epe.ed.tum.de/ens/research/projects/current-projects/need/) and the project [NFDI4Energy](https://nfdi4energy.de/).

# Contact

[info@dvg.tu-berlin.de](mailto:info@dvg.tu-berlin.de)
