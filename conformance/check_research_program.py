"""Check research queue references and boundaries without promoting claims."""

from datetime import date
import json
from pathlib import Path
import re
import tomllib
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def local_file(path):
    require(isinstance(path, str) and path, "missing local path")
    resolved = (ROOT / path).resolve()
    require(resolved.is_relative_to(ROOT) and resolved.is_file(),
            f"missing/outside repository file: {path}")
    return resolved


def unique_records(records, label):
    answer = {}
    for record in records:
        key = record["id"]
        require(isinstance(key, str) and key and key not in answer, f"invalid/duplicate {label}")
        answer[key] = record
    return answer


def main():
    program = tomllib.loads(local_file("docs/research/program.toml").read_text())
    require(program["schema"] == 1 and program["acceptance_authority"] is False,
            "research planning cannot acquire acceptance authority")
    require(program["authority"] == "exposition_and_experiment_planning", "wrong authority")
    date.fromisoformat(program["updated"])
    for key in ("brief", "roadmap", "sources", "seed_experiment", "seed_fixture", "seed_receipt"):
        local_file(program[key])
    catalog = tomllib.loads(local_file(program["sources"]).read_text())
    require(catalog["schema"] == 1, "unsupported source catalog schema")
    date.fromisoformat(catalog["checked_on"])
    sources = unique_records(catalog["source"], "source")
    for source in sources.values():
        for key in ("title", "locator", "supports", "boundary"):
            require(isinstance(source[key], str) and source[key], f"missing source {key}")
        for key in ("url", "read_url"):
            url = urlsplit(source[key])
            require(url.scheme == "https" and url.netloc, "invalid source URL")

    claims = unique_records(tomllib.loads(local_file("proof/claims.toml").read_text())["claim"], "claim")
    for key, status in program["baseline_claims"].items():
        require(key in claims and claims[key]["status"] == status, f"baseline claim drift: {key}")
    questions = unique_records(program["question"], "question")
    require(not (set(questions) & set(claims)), "research questions must have separate IDs")
    next_question = questions[program["next_question"]]
    require(next_question["status"] == "active", "next question is not active")
    brief = local_file(program["brief"]).read_text()
    priorities = []
    for key, question in questions.items():
        require(key in brief, f"question has no human-readable brief: {key}")
        require(question["status"] in ("active", "queued"), "unsupported question state")
        require(question["kind"] in ("repository_research_task", "repository_research_question",
                                     "published_question_status_audit",
                                     "published_problem_and_repository_extension"), "unsupported question kind")
        require(type(question["priority"]) is int and question["priority"] > 0,
                "priority must be a positive integer")
        priorities.append(question["priority"])
        for field in ("title", "scope", "first_action"):
            require(isinstance(question[field], str) and question[field], f"missing {field}")
        for field in ("acceptance", "falsification", "sources"):
            require(question[field] and all(isinstance(s, str) and s for s in question[field]),
                    f"missing {field}")
        require(set(question["sources"]) <= set(sources), f"unknown source: {key}")
        dependencies = question["dependencies"]
        require(len(dependencies) == len(set(dependencies)) and key not in dependencies,
                "duplicate or self dependency")
        require(set(dependencies) <= (set(questions) | set(claims)), "unknown dependency")
    require(len(priorities) == len(set(priorities)), "ambiguous priorities")

    complete, visiting = set(), set()

    def visit(key):
        require(key not in visiting, "research dependency cycle")
        if key in complete:
            return
        visiting.add(key)
        for dependency in questions[key]["dependencies"]:
            if dependency in questions:
                visit(dependency)
        visiting.remove(key)
        complete.add(key)

    for key in questions:
        visit(key)

    receipt = json.loads(local_file(program["seed_receipt"]).read_text())
    require(receipt["authority"] == "non_authoritative_experiment"
            and receipt["claim_promotions"] == [], "seed experiment cannot promote claims")
    require(set(receipt["questions"]) <= set(questions), "receipt references unknown questions")
    # Validate the edited navigation and brief. Links to prior dated
    # evidence remain historical and are not rewritten by this scaffold.
    for name in (program["brief"], program["roadmap"], "README.md", "sources/README.md",
                 "experiments/README.md", "conformance/README.md"):
        doc = local_file(name)
        for link in re.findall(r"\]\(([^)]+)\)", doc.read_text()):
            if urlsplit(link).scheme or link.startswith("#"):
                continue
            target = (doc.parent / link.split("#", 1)[0]).resolve()
            require(target.is_relative_to(ROOT) and target.exists(), f"broken local link: {name}: {link}")
    print(f"PASS: {len(questions)} research questions, {len(sources)} primary sources; "
          "baseline states, dependencies, evidence, and local navigation validate")


if __name__ == "__main__":
    main()
