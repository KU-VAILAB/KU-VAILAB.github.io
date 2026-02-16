# VAI Lab Website

This website is built with [Jekyll](https://jekyllrb.com/).
It is derived from the template provided by the [Allan Lab](https://www.allanlab.org/aboutwebsite.html) at Leiden University.

## Setup

This repository is tested under `ruby 3.1.0`, `bundler 2.3.3`.
If the setup crashes, remove `Gemfile.lock` and run the setup again.

``` bash
brew install ruby
gem install bundler jekyll
```

Then install the dependencies:

``` bash
bundle install
```

## Run

Run the local webserver with:

``` bash
bundle exec jekyll serve
```

## Maintenance

Most of the website data is managed through CSV files and Python scripts. The general workflow follows the pattern: **CSV File** ➔ **Python Script** ➔ **Generated Data**.

All source files are stored on Google Drive and managed via Google Forms, which are accessible only via the shared VAI Google account. If you do not have the credentials, please contact the PI.

Updates are automatically deployed to the website once changes are pushed to the `master` branch.

### 1. Adding a Member
Use this to update the current lab members (Students/Interns).
Team Page uses each mardown file to render each member.
- **Source**: `_data/members.csv`, exported from the Google Sheet: `VAI-Lab Homepage 용 인적사항 수합(응답)`. This sheet is linked to the Google Form: `VAI-Lab Homepage 용 인적사항 수합`.
- **Action**: Add a new row to the CSV.
- **Run**: `python3 scripts/generate_members.py`
- **Result**: New Markdown files are generated in `_pages/team/_posts/`.

### 2. Adding Alumni
Use this to update the lab alumni list.
- **Source**: `_data/alumni.csv`, exported from the Google Sheet: `VAI 연락망`.
- **Required Columns**: `영문 이름` (English Name) and `비고 (영문)` (Affiliation/Remarks in English).
- **Run**: `python3 scripts/generate_alumni.py`
- **Result**: Markdown files are generated in `_pages/team/_posts/` with `category: alumni`.

### 3. Adding Funding & Sponsors
Update the logos shown on the Research page.
- **Source**: Drop image files (PNG, JPG, etc.) into `images/research/Fundings/`.
- **Run**: `python3 scripts/generate_fundings.py`
- **Result**: Updates `_data/fundings.yml`, which the Research page uses to render the logo grid.

### 4. Adding Publications
Use this to update the Publications page.
- **Source**: `_data/raw_publications.csv`, exported from the Google Sheet: `VAI: 실적취합`.
- **Format**: `Title,Authors,Conference,Link`. Use semicolons (`;`) to separate multiple authors.
- **Run**: `python3 scripts/parse_publications.py`
- **Result**: Converts the CSV to `_data/publications.json` (CSL-JSON format) for website display.
