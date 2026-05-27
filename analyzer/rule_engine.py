# Contains IaC rule checks
def check_s3_bucket_acl(resources):
    issues = []
    for item in resources:
        if "aws_s3_bucket" in item:
            for name, config in item["aws_s3_bucket"].items():
                acl = config.get("acl", "")
                if acl in ["public-read", "public-write"]:
                    issues.append(f"❌ S3 Bucket '{name}' has insecure ACL: '{acl}'")
    return issues


def check_ec2_name_tag(resources):
    issues = []
    for item in resources:
        if "aws_instance" in item:
            for name, config in item["aws_instance"].items():
                tags = config.get("tags", {})
                if "Name" not in tags:
                    issues.append(f"⚠️ EC2 Instance '{name}' is missing a 'Name' tag")
    return issues


def run_all_checks(blocks):
    resources = blocks.get("resource", [])
    all_issues = []

    all_issues.extend(check_s3_bucket_acl(resources))
    all_issues.extend(check_ec2_name_tag(resources))

    return all_issues


# Example usage (only for testing from CLI)
if __name__ == "__main__":
    from terraform_parser import parse_terraform_file, extract_blocks

    tf_file = "../examples/main.tf"
    parsed = parse_terraform_file(tf_file)
    blocks = extract_blocks(parsed)

    issues = run_all_checks(blocks)
    if not issues:
        print("✅ No issues found.")
    else:
        print("🔍 Issues detected:")
        for issue in issues:
            print(" -", issue)
