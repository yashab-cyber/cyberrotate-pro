# Contributing to CyberRotate Pro Manual

Thank you for your interest in contributing to the CyberRotate Pro documentation! This document provides guidelines for contributing to the manual.

## 📋 Table of Contents

1. [How to Contribute](#how-to-contribute)
2. [Documentation Standards](#documentation-standards)
3. [File Organization](#file-organization)
4. [Writing Guidelines](#writing-guidelines)
5. [Review Process](#review-process)
6. [Style Guide](#style-guide)

## 🤝 How to Contribute

### Types of Contributions

We welcome the following types of contributions:

- **Bug Fixes**: Corrections to errors in documentation
- **Content Updates**: Adding new features or updating existing content
- **Translations**: Translating documentation to other languages
- **Examples**: Adding code examples and use cases
- **Improvements**: Enhancing clarity and readability

### Getting Started

1. **Fork the Repository**: Create a fork of the documentation repository
2. **Create a Branch**: Create a feature branch for your changes
3. **Make Changes**: Edit the relevant markdown files
4. **Test Changes**: Verify all links and formatting work correctly
5. **Submit Pull Request**: Submit your changes for review

## 📚 Documentation Standards

### File Naming Convention

All documentation files follow a specific naming pattern:

```
##-filename.md
```

Where:
- `##` is a two-digit number (01-20)
- `filename` is a descriptive name using lowercase and hyphens
- `.md` is the markdown extension

Examples:
- `01-installation.md`
- `06-api-reference.md`
- `14-troubleshooting.md`

### Required Sections

Each documentation file should include:

1. **Title**: Clear, descriptive title using H1 (`#`)
2. **Table of Contents**: Numbered list of main sections
3. **Introduction**: Brief overview of the content
4. **Main Content**: Detailed information organized in sections
5. **Examples**: Code examples and practical demonstrations
6. **Additional Resources**: Links to related documentation
7. **Footer**: Reference to main manual page

### Markdown Structure

```markdown
# Page Title

Brief description of the page content.

## 📋 Table of Contents

1. [Section One](#section-one)
2. [Section Two](#section-two)
3. [Examples](#examples)

---

## Section One

Content here...

### Subsection

More detailed content...

## Examples

```code
example code here
```

---

## 📖 Additional Resources

- Link to related pages
- External resources

---

*This guide is part of the CyberRotate Pro manual. For more information, visit the [main manual page](README.md).*
```

## 📁 File Organization

### Current Structure

```
manual/
├── README.md                 # Main manual index
├── RELEASE_NOTES.md         # Release information
├── CONTRIBUTING.md          # This file
├── 01-installation.md       # Installation guide
├── 02-quick-start.md        # Quick start guide
├── 03-configuration.md      # Configuration options
├── 04-gui-guide.md         # GUI user guide
├── 05-cli-guide.md         # CLI user guide
├── 06-api-reference.md     # API documentation
├── 07-vpn-setup.md         # VPN configuration
├── 08-proxy-management.md  # Proxy management
├── 09-tor-integration.md   # Tor integration
├── 10-security.md          # Security features
├── 11-performance.md       # Performance optimization
├── 12-analytics.md         # Analytics and reporting
├── 13-automation.md        # Automation features
├── 14-troubleshooting.md   # Troubleshooting guide
├── 15-debugging.md         # Debug techniques
├── 16-faq.md              # Frequently asked questions
├── 17-support.md          # Support information
├── 18-developer.md        # Developer guide
├── 19-api-examples.md     # API code examples
└── 20-enterprise.md       # Enterprise features
```

### Adding New Files

When adding new documentation files:

1. Follow the numbering convention
2. Update the main `README.md` table of contents
3. Add cross-references from related files
4. Include the file in the appropriate section

## ✍️ Writing Guidelines

### Tone and Style

- **Clear and Concise**: Use simple, direct language
- **Professional**: Maintain a professional but friendly tone
- **Inclusive**: Use inclusive language and examples
- **Action-Oriented**: Focus on what users need to do
- **Consistent**: Follow established patterns and terminology

### Technical Writing Best Practices

#### Use Active Voice
```markdown
✅ "Configure the VPN settings"
❌ "The VPN settings should be configured"
```

#### Write Clear Instructions
```markdown
✅ "1. Open the configuration file
    2. Add your API key
    3. Save the file"
    
❌ "You might want to consider opening the config file and adding your key"
```

#### Provide Context
```markdown
✅ "Use HTTPS proxies for better security when handling sensitive data"
❌ "Use HTTPS proxies"
```

### Code Examples

#### Format Code Blocks
```markdown
```python
# Python example
import cyberrotate

client = cyberrotate.Client(api_key="your-key")
result = client.rotate_ip()
```
```

#### Include Context
```markdown
The following example shows how to rotate IP addresses programmatically:

```python
# This example assumes you have configured your API key
import cyberrotate

client = cyberrotate.Client(api_key="your-api-key")
result = client.rotate_ip()

if result.success:
    print(f"New IP: {result.ip}")
else:
    print(f"Error: {result.error}")
```
```

### Screenshots and Images

When including images:

1. Use descriptive file names
2. Store in an `images/` subdirectory
3. Provide alt text for accessibility
4. Include captions when helpful

```markdown
![VPN Configuration Interface](images/vpn-config-interface.png)
*The VPN configuration interface showing server selection options*
```

## 🔍 Review Process

### Before Submitting

1. **Spell Check**: Run a spell checker on your content
2. **Link Verification**: Ensure all links work correctly
3. **Code Testing**: Test all code examples
4. **Cross-References**: Update related documentation
5. **Table of Contents**: Update TOC if adding new sections

### Pull Request Guidelines

#### Title Format
```
type(scope): brief description

Examples:
- docs(installation): add Docker installation steps
- fix(api): correct endpoint URL in examples
- update(security): add new leak protection features
```

#### Description Template
```markdown
## Summary
Brief description of changes

## Changes Made
- List of specific changes
- Include any new files added
- Note any files deleted or moved

## Testing
- Verified all links work
- Tested code examples
- Checked formatting

## Related Issues
- Closes #123
- Addresses feedback from #456
```

### Review Criteria

Reviewers will check for:

- **Accuracy**: Technical accuracy of content
- **Completeness**: All necessary information included
- **Clarity**: Easy to understand and follow
- **Consistency**: Matches existing style and format
- **Links**: All internal and external links work
- **Examples**: Code examples are correct and tested

## 🎨 Style Guide

### Headers

Use descriptive headers with emoji prefixes:

```markdown
# Main Title
## 📋 Table of Contents
## 🚀 Getting Started
## ⚙️ Configuration
## 💡 Examples
## 🔧 Troubleshooting
## 📖 Additional Resources
```

### Lists

Use numbered lists for sequential steps:
```markdown
1. First step
2. Second step
3. Third step
```

Use bullet points for non-sequential items:
```markdown
- Feature one
- Feature two
- Feature three
```

### Emphasis

- Use **bold** for important terms and UI elements
- Use *italics* for emphasis and file names
- Use `code formatting` for commands, file names, and code snippets

### Links

#### Internal Links
```markdown
[Configuration Guide](03-configuration.md)
[API Reference](06-api-reference.md#authentication)
```

#### External Links
```markdown
[Official Website](https://zehrasec.com)
[GitHub Repository](https://github.com/zehrasec/cyberrotate)
```

### Code Blocks

Always specify the language for syntax highlighting:

```markdown
```python
# Python code
```

```bash
# Shell commands
```

```json
{
  "configuration": "example"
}
```
```

### Tables

Use tables for structured data:

```markdown
| Feature | Personal | Business | Enterprise |
|---------|----------|----------|------------|
| Users   | 1        | 10       | Unlimited  |
| Support | Email    | Priority | 24/7       |
```

### Callouts

Use appropriate callouts for different types of information:

```markdown
> **Note**: This is general information

> **Warning**: This is important safety information

> **Tip**: This is a helpful suggestion
```

## 🌍 Translations

### Adding Translations

1. Create a new directory: `manual/[language-code]/`
2. Copy all markdown files to the new directory
3. Translate content while maintaining structure
4. Update the main README to link to translations

### Translation Guidelines

- Maintain the same file structure and naming
- Keep code examples in English unless localization is needed
- Translate UI elements and error messages
- Maintain consistency in technical terminology

## 📞 Getting Help

If you need help with contributing:

1. **Documentation Issues**: Open an issue on GitHub
2. **Questions**: Ask in our community Discord
3. **Email**: Contact documentation team at docs@zehrasec.com

## 📝 License

By contributing to this documentation, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for helping make CyberRotate Pro documentation better for everyone!

*For more information about the project, visit the [main manual page](README.md).*
