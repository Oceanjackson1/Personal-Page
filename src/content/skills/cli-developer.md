---
title: "CLI Developer"
description: "Use when building CLI tools, implementing argument parsing, or adding interactive prompts. Invoke for parsing flags and subcommands, displaying progress bars and spinners, generating bash/zsh/fish completion scripts, CLI design, shell completions,..."
category: "devops"
source: "community"
author: "Community"
tags: ["cli", "developer"]
date: 2026-03-20
---

# CLI Developer

## Core Workflow

1. **Analyze UX** — Identify user workflows, command hierarchy, common tasks. Validate by listing all commands and their expected `--help` output before writing code.
2. **Design commands** — Plan subcommands, flags, arguments, configuration. Confirm flag naming is consistent and no existing signatures are broken.
3. **Implement** — Build with the appropriate CLI framework for the language (see Reference Guide below). After wiring up commands, run `<cli> --help` to verify help text renders correctly and `<cli> --version` to confirm version output.
4. **Polish** — Add completions, help text, error messages, progress indicators. Verify TTY detection for color output and graceful SIGINT handling.
5. **Test** — Run cross-platform smoke tests; benchmark startup time (target: <50ms).

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Design Patterns | `references/design-patterns.md` | Subcommands, flags, config, architecture |
| Node.js CLIs | `references/node-cli.md` | commander, yargs, inquirer, chalk |
| Python CLIs | `references/python-cli.md` | click, typer, argparse, rich |
| Go CLIs | `references/go-cli.md` | cobra, viper, bubbletea |
| UX Patterns | `references/ux-patterns.md` | Progress bars, colors, help text |

## Quick-Start Example

### Node.js (commander)

```js
#!/usr/bin/env node
// npm install commander
const { program } = require('commander');

program
  .name('mytool')
  .description('Example CLI')
  .version('1.0.0');

program
  .command('greet <name>')
  .description('Greet a user')
  .option('-l, --loud', 'uppercase the greeting')
  .action((name, opts) => {
    const msg = `Hello, ${name}!`;
    console.log(opts.loud ? msg.toUpperCase() : msg);
  });

program.parse();
```

For Python (click/typer) and Go (cobra) quick-start examples, see `references/python-cli.md` and `references/go-cli.md`.

## Constraints

### MUST DO
- Keep startup time under 50ms
- Provide clear, actionable error messages
- Support `--help` and `--version` flags
- Use consistent flag naming conventions
- Handle SIGINT (Ctrl+C) gracefully
- Validate user input early
- Support both interactive and non-interactive modes
- Test on Windows, macOS, and Linux

### MUST NOT DO

- **Block on synchronous I/O unnecessarily** — use async reads or stream processing instead.
- **Print to stdout when output will be piped** — write logs/diagnostics to stderr.
- **Use colors when output is not a TTY** — detect before applying color:
  ```js
  // Node.js
  const useColor = process.stdout.isTTY;
  ```
  ```python
  # Python
  import sys
  use_color = sys.stdout.isatty()
  ```
  ```go
  // Go
  import "golang.org/x/term"
  useColor := term.IsTerminal(int(os.Stdout.Fd()))
  ```
- **Break existing command signatures** — treat flag/subcommand renames as breaking changes.
- **Require interactive input in CI/CD environments** — always provide non-interactive fallbacks via flags or env vars.
- **Hardcode paths or platform-specific logic** — use `os.homedir()` / `os.UserHomeDir()` / `Path.home()` instead.
- **Ship without shell completions** — all three frameworks above have built-in completion generation.

## Output Templates

When implementing CLI features, provide:
1. Command structure (main entry point, subcommands)
2. Configuration handling (files, env vars, flags)
3. Core implementation with error handling
4. Shell completion scripts if applicable
5. Brief explanation of UX decisions

## Knowledge Reference

CLI frameworks (commander, yargs, oclif, click, typer, argparse, cobra, viper), terminal UI (chalk, inquirer, rich, bubbletea), testing (snapshot testing, E2E), distribution (npm, pip, homebrew, releases), performance optimization

---

## Reference: Design Patterns

# CLI Design Patterns

## Command Hierarchy

```
mycli                           # Root command
├── init [options]              # Simple command
├── config
│   ├── get <key>              # Nested subcommand
│   ├── set <key> <value>
│   └── list
├── deploy [environment]        # Command with args
│   ├── --dry-run              # Flag
│   ├── --force
│   └── --config <file>        # Option with value
└── plugins
    ├── install <name>
    ├── list
    └── remove <name>
```

## Flag Conventions

```bash
# Boolean flags (presence = true)
mycli deploy --force --dry-run

# Short + long forms
mycli -v --verbose
mycli -c config.yml --config config.yml

# Required vs optional
mycli deploy <env>              # Positional (required)
mycli deploy --env production   # Flag (optional)

# Multiple values
mycli install pkg1 pkg2 pkg3    # Variadic args
mycli --exclude node_modules --exclude .git
```

## Configuration Layers

Priority order (highest to lowest):

1. **Command-line flags** - Explicit user intent
2. **Environment variables** - Runtime context
3. **Config files (project)** - `.myclirc`, `mycli.config.js`
4. **Config files (user)** - `~/.myclirc`, `~/.config/mycli/config.yml`
5. **Config files (system)** - `/etc/mycli/config.yml`
6. **Defaults** - Hard-coded sensible defaults

```javascript
// Example config resolution
const config = {
  ...systemDefaults,
  ...loadSystemConfig(),
  ...loadUserConfig(),
  ...loadProjectConfig(),
  ...loadEnvVars(),
  ...parseCliFlags(),
};
```

## Exit Codes

Standard POSIX exit codes:

```javascript
const EXIT_CODES = {
  SUCCESS: 0,
  GENERAL_ERROR: 1,
  MISUSE: 2,              // Invalid arguments
  PERMISSION_DENIED: 77,
  NOT_FOUND: 127,
  SIGINT: 130,            // Ctrl+C
};
```

## Plugin Architecture

```
mycli/
├── core/                      # Core functionality
├── plugins/
│   ├── aws/                  # Plugin: AWS integration
│   │   ├── package.json
│   │   └── index.js
│   └── github/               # Plugin: GitHub integration
│       ├── package.json
│       └── index.js
└── plugin-loader.js          # Discovery & loading
```

Plugin discovery:
1. Check `~/.mycli/plugins/`
2. Check `node_modules/mycli-plugin-*`
3. Check `MYCLI_PLUGIN_PATH` env var

## Error Handling Patterns

```javascript
// Good: Actionable error messages
Error: Config file not found at /path/to/config.yml

Tried locations:
  • ./mycli.config.yml
  • ~/.myclirc
  • /etc/mycli/config.yml

Run 'mycli init' to create a config file, or use --config to specify location.

// Bad: Unhelpful errors
Error: ENOENT
```

## Interactive vs Non-Interactive

```javascript
// Detect if running in CI/CD
const isCI = process.env.CI === 'true' || !process.stdout.isTTY;

if (isCI) {
  // Non-interactive: fail fast with clear errors
  if (!options.environment) {
    throw new Error('--environment required in non-interactive mode');
  }
} else {
  // Interactive: prompt user
  const environment = await prompt({
    type: 'select',
    message: 'Select environment:',
    choices: ['development', 'staging', 'production'],
  });
}
```

## State Management

```
~/.mycli/
├── config.yml           # User configuration
├── cache/               # Cached data
│   ├── plugins.json
│   └── api-responses/
├── credentials.json     # Sensitive data (600 perms)
└── state.json          # Session state
```

## Performance Patterns

```javascript
// Lazy loading: Don't load unused dependencies
if (command === 'deploy') {
  const deploy = require('./commands/deploy'); // Load on demand
  await deploy.run();
}

// Caching: Avoid repeated API calls
const cache = new Cache('~/.mycli/cache', { ttl: 3600 });
let plugins = await cache.get('plugins');
if (!plugins) {
  plugins = await fetchPlugins();
  await cache.set('plugins', plugins);
}

// Async operations: Don't block unnecessarily
await Promise.all([
  validateConfig(),
  checkForUpdates(),
  loadPlugins(),
]);
```

## Versioning & Updates

```javascript
// Check for updates (non-blocking)
checkForUpdates().then(update => {
  if (update.available) {
    console.log(`Update available: ${update.version}`);
    console.log(`Run: npm install -g mycli@latest`);
  }
}).catch(() => {
  // Silently fail - don't interrupt user workflow
});

// Version compatibility
const MIN_NODE_VERSION = '18.0.0';
if (!semver.satisfies(process.version, `>=${MIN_NODE_VERSION}`)) {
  console.error(`mycli requires Node.js ${MIN_NODE_VERSION} or higher`);
  process.exit(1);
}
```

## Help Text Design

```
USAGE
  mycli deploy [environment] [options]

ARGUMENTS
  environment  Target environment (development|staging|production)

OPTIONS
  -c, --config <file>  Path to config file
  -f, --force          Skip confirmation prompts
  -d, --dry-run        Preview changes without executing
  -v, --verbose        Show detailed output

EXAMPLES
  # Deploy to production
  mycli deploy production

  # Preview staging deployment
  mycli deploy staging --dry-run

  # Use custom config
  mycli deploy --config ./custom.yml

Learn more: https://docs.mycli.dev/deploy
```

---

## Reference: Go Cli

# Go CLI Development

## Cobra (Recommended)

Powerful CLI framework used by kubectl, hugo, docker.

```go
// cmd/root.go
package cmd

import (
    "fmt"
    "os"
    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)

var (
    cfgFile string
    verbose bool
)

var rootCmd = &cobra.Command{
    Use:   "mycli",
    Short: "My awesome CLI tool",
    Long: `A longer description of your CLI application`,
    Version: "1.0.0",
}

func Execute() {
    if err := rootCmd.Execute(); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}

func init() {
    cobra.OnInitialize(initConfig)

    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file")
    rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")

    viper.BindPFlag("verbose", rootCmd.PersistentFlags().Lookup("verbose"))
}

func initConfig() {
    if cfgFile != "" {
        viper.SetConfigFile(cfgFile)
    } else {
        home, err := os.UserHomeDir()
        cobra.CheckErr(err)

        viper.AddConfigPath(home)
        viper.AddConfigPath(".")
        viper.SetConfigType("yaml")
        viper.SetConfigName(".mycli")
    }

    viper.AutomaticEnv()

    if err := viper.ReadInConfig(); err == nil {
        fmt.Fprintln(os.Stderr, "Using config file:", viper.ConfigFileUsed())
    }
}

// cmd/init.go
package cmd

import (
    "fmt"
    "github.com/spf13/cobra"
)

var (
    template string
    force    bool
)

var initCmd = &cobra.Command{
    Use:   "init [name]",
    Short: "Initialize a new project",
    Args:  cobra.ExactArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        name := args[0]
        return initProject(name, template, force)
    },
}

func init() {
    rootCmd.AddCommand(initCmd)

    initCmd.Flags().StringVarP(&template, "template", "t", "default", "Project template")
    initCmd.Flags().BoolVarP(&force, "force", "f", false, "Overwrite existing")
}

func initProject(name, template string, force bool) error {
    fmt.Printf("Creating %s from %s\n", name, template)
    return nil
}

// cmd/deploy.go
package cmd

import (
    "fmt"
    "github.com/spf13/cobra"
)

var (
    dryRun bool
)

var deployCmd = &cobra.Command{
    Use:   "deploy [environment]",
    Short: "Deploy to environment",
    Args:  cobra.ExactArgs(1),
    ValidArgs: []string{"dev", "staging", "prod"},
    RunE: func(cmd *cobra.Command, args []string) error {
        env := args[0]
        return deploy(env, dryRun)
    },
}

func init() {
    rootCmd.AddCommand(deployCmd)
    deployCmd.Flags().BoolVar(&dryRun, "dry-run", false, "Preview only")
}

func deploy(env string, dryRun bool) error {
    if dryRun {
        fmt.Printf("Would deploy to: %s\n", env)
    } else {
        fmt.Printf("Deploying to %s...\n", env)
    }
    return nil
}

// main.go
package main

import "mycli/cmd"

func main() {
    cmd.Execute()
}
```

## Viper (Configuration)

Configuration management with multiple sources.

```go
package config

import (
    "fmt"
    "github.com/spf13/viper"
)

type Config struct {
    Environment string `mapstructure:"environment"`
    Timeout     int    `mapstructure:"timeout"`
    Verbose     bool   `mapstructure:"verbose"`
    API         APIConfig `mapstructure:"api"`
}

type APIConfig struct {
    Endpoint string `mapstructure:"endpoint"`
    Token    string `mapstructure:"token"`
}

func Load() (*Config, error) {
    // Set defaults
    viper.SetDefault("environment", "development")
    viper.SetDefault("timeout", 30)
    viper.SetDefault("verbose", false)

    // Config file locations
    viper.SetConfigName("config")
    viper.SetConfigType("yaml")
    viper.AddConfigPath("/etc/mycli/")
    viper.AddConfigPath("$HOME/.config/mycli")
    viper.AddConfigPath(".")

    // Environment variables
    viper.SetEnvPrefix("MYCLI")
    viper.AutomaticEnv()

    // Read config
    if err := viper.ReadInConfig(); err != nil {
        if _, ok := err.(viper.ConfigFileNotFoundError); !ok {
            return nil, fmt.Errorf("failed to read config: %w", err)
        }
    }

    // Unmarshal into struct
    var cfg Config
    if err := viper.Unmarshal(&cfg); err != nil {
        return nil, fmt.Errorf("failed to unmarshal config: %w", err)
    }

    return &cfg, nil
}
```

## Bubble Tea (Interactive TUI)

Modern terminal UI framework for interactive CLIs.

```go
package main

import (
    "fmt"
    "os"

    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

// Model
type model struct {
    choices  []string
    cursor   int
    selected map[int]struct{}
}

func initialModel() model {
    return model{
        choices:  []string{"TypeScript", "ESLint", "Prettier", "Jest"},
        selected: make(map[int]struct{}),
    }
}

// Init
func (m model) Init() tea.Cmd {
    return nil
}

// Update
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            return m, tea.Quit

        case "up", "k":
            if m.cursor > 0 {
                m.cursor--
            }

        case "down", "j":
            if m.cursor < len(m.choices)-1 {
                m.cursor++
            }

        case " ":
            _, ok := m.selected[m.cursor]
            if ok {
                delete(m.selected, m.cursor)
            } else {
                m.selected[m.cursor] = struct{}{}
            }

        case "enter":
            return m, tea.Quit
        }
    }

    return m, nil
}

// View
func (m model) View() string {
    s := "Select features:\n\n"

    for i, choice := range m.choices {
        cursor := " "
        if m.cursor == i {
            cursor = ">"
        }

        checked := " "
        if _, ok := m.selected[i]; ok {
            checked = "x"
        }

        s += fmt.Sprintf("%s [%s] %s\n", cursor, checked, choice)
    }

    s += "\nPress space to select, enter to confirm, q to quit.\n"

    return s
}

func main() {
    p := tea.NewProgram(initialModel())
    if _, err := p.Run(); err != nil {
        fmt.Printf("Error: %v", err)
        os.Exit(1)
    }
}
```

## Progress Indicators

```go
package main

import (
    "fmt"
    "time"

    "github.com/schollz/progressbar/v3"
)

func main() {
    // Simple progress bar
    bar := progressbar.Default(100, "Downloading")
    for i := 0; i < 100; i++ {
        bar.Add(1)
        time.Sleep(40 * time.Millisecond)
    }

    // Custom progress bar
    bar = progressbar.NewOptions(100,
        progressbar.OptionEnableColorCodes(true),
        progressbar.OptionShowBytes(true),
        progressbar.OptionSetWidth(15),
        progressbar.OptionSetDescription("[cyan][1/3][reset] Downloading..."),
        progressbar.OptionSetTheme(progressbar.Theme{
            Saucer:        "[green]=[reset]",
            SaucerHead:    "[green]>[reset]",
            SaucerPadding: " ",
            BarStart:      "[",
            BarEnd:        "]",
        }),
    )

    for i := 0; i < 100; i++ {
        bar.Add(1)
        time.Sleep(40 * time.Millisecond)
    }
}
```

## Spinner

```go
package main

import (
    "fmt"
    "time"

    "github.com/briandowns/spinner"
)

func main() {
    s := spinner.New(spinner.CharSets[11], 100*time.Millisecond)
    s.Suffix = " Installing dependencies..."
    s.Start()

    time.Sleep(4 * time.Second)

    s.UpdateCharSet(spinner.CharSets[9])
    s.Suffix = " Processing..."
    time.Sleep(2 * time.Second)

    s.Stop()
    fmt.Println("✓ Done!")
}
```

## Colored Output

```go
package main

import (
    "github.com/fatih/color"
)

func main() {
    // Basic colors
    color.Blue("Info: Starting deployment...")
    color.Green("Success: Deployment complete!")
    color.Yellow("Warning: Deprecated flag used")
    color.Red("Error: Deployment failed")

    // Custom styles
    success := color.New(color.FgGreen, color.Bold).PrintlnFunc()
    error := color.New(color.FgRed, color.Bold).PrintlnFunc()

    success("✓ Build successful")
    error("✗ Build failed")

    // Printf-style
    color.Cyan("Processing %d files...\n", 42)

    // Disable colors for CI
    if os.Getenv("CI") != "" {
        color.NoColor = true
    }
}
```

## Error Handling

```go
package main

import (
    "errors"
    "fmt"
    "os"
    "syscall"

    "github.com/spf13/cobra"
)

var deployCmd = &cobra.Command{
    Use:   "deploy",
    Short: "Deploy application",
    RunE: func(cmd *cobra.Command, args []string) error {
        if err := deploy(); err != nil {
            return handleError(err)
        }
        return nil
    },
}

func handleError(err error) error {
    var exitCode int

    switch {
    case errors.Is(err, os.ErrPermission):
        fmt.Fprintln(os.Stderr, "Permission denied")
        fmt.Fprintln(os.Stderr, "Try running with sudo or check file permissions")
        exitCode = 77

    case errors.Is(err, os.ErrNotExist):
        fmt.Fprintf(os.Stderr, "File not found: %v\n", err)
        exitCode = 127

    default:
        fmt.Fprintf(os.Stderr, "Deployment failed: %v\n", err)
        if os.Getenv("DEBUG") != "" {
            fmt.Fprintf(os.Stderr, "%+v\n", err)
        }
        exitCode = 1
    }

    os.Exit(exitCode)
    return nil
}

// Handle SIGINT (Ctrl+C)
func main() {
    // Setup signal handling
    c := make(chan os.Signal, 1)
    signal.Notify(c, os.Interrupt, syscall.SIGTERM)

    go func() {
        <-c
        fmt.Println("\nOperation cancelled")
        os.Exit(130)
    }()

    cmd.Execute()
}
```

## Testing

```go
package cmd

import (
    "bytes"
    "testing"

    "github.com/spf13/cobra"
    "github.com/stretchr/testify/assert"
)

func TestInitCommand(t *testing.T) {
    cmd := &cobra.Command{Use: "test"}
    cmd.AddCommand(initCmd)

    b := bytes.NewBufferString("")
    cmd.SetOut(b)
    cmd.SetArgs([]string{"init", "my-project"})

    err := cmd.Execute()
    assert.NoError(t, err)
    assert.Contains(t, b.String(), "Creating my-project")
}

func TestInitWithTemplate(t *testing.T) {
    cmd := &cobra.Command{Use: "test"}
    cmd.AddCommand(initCmd)

    b := bytes.NewBufferString("")
    cmd.SetOut(b)
    cmd.SetArgs([]string{"init", "my-project", "--template", "react"})

    err := cmd.Execute()
    assert.NoError(t, err)
    assert.Contains(t, b.String(), "react")
}
```

## Build & Distribution

```makefile
# Makefile
VERSION := $(shell git describe --tags --always --dirty)
LDFLAGS := -ldflags "-X main.version=$(VERSION)"

.PHONY: build
build:
	go build $(LDFLAGS) -o bin/mycli main.go

.PHONY: install
install:
	go install $(LDFLAGS)

.PHONY: test
test:
	go test -v ./...

.PHONY: release
release:
	GOOS=linux GOARCH=amd64 go build $(LDFLAGS) -o bin/mycli-linux-amd64
	GOOS=darwin GOARCH=amd64 go build $(LDFLAGS) -o bin/mycli-darwin-amd64
	GOOS=darwin GOARCH=arm64 go build $(LDFLAGS) -o bin/mycli-darwin-arm64
	GOOS=windows GOARCH=amd64 go build $(LDFLAGS) -o bin/mycli-windows-amd64.exe
```

---

## Reference: Node Cli

# Node.js CLI Development

## Commander.js (Recommended)

Modern, elegant CLI framework with TypeScript support.

```javascript
#!/usr/bin/env node
import { Command } from 'commander';
import { version } from './package.json';

const program = new Command();

program
  .name('mycli')
  .description('My awesome CLI tool')
  .version(version);

// Simple command
program
  .command('init')
  .description('Initialize a new project')
  .option('-t, --template <type>', 'Project template', 'default')
  .option('-f, --force', 'Overwrite existing files')
  .action(async (options) => {
    console.log(`Initializing with template: ${options.template}`);
  });

// Command with arguments
program
  .command('deploy <environment>')
  .description('Deploy to environment')
  .option('--dry-run', 'Preview without executing')
  .action(async (environment, options) => {
    if (options.dryRun) {
      console.log(`Would deploy to: ${environment}`);
    } else {
      await deploy(environment);
    }
  });

// Nested subcommands
const config = program.command('config').description('Manage configuration');

config
  .command('get <key>')
  .description('Get config value')
  .action((key) => console.log(getConfig(key)));

config
  .command('set <key> <value>')
  .description('Set config value')
  .action((key, value) => setConfig(key, value));

program.parse();
```

## Yargs (Alternative)

Powerful argument parsing with middleware support.

```javascript
#!/usr/bin/env node
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

yargs(hideBin(process.argv))
  .command(
    'deploy <env>',
    'Deploy to environment',
    (yargs) => {
      return yargs
        .positional('env', {
          describe: 'Environment name',
          choices: ['dev', 'staging', 'prod'],
        })
        .option('force', {
          alias: 'f',
          type: 'boolean',
          description: 'Force deployment',
        });
    },
    async (argv) => {
      await deploy(argv.env, { force: argv.force });
    }
  )
  .middleware([(argv) => {
    // Validate before all commands
    if (!isConfigValid()) {
      throw new Error('Invalid config');
    }
  }])
  .demandCommand()
  .help()
  .parse();
```

## Interactive Prompts (Inquirer)

Beautiful interactive prompts for user input.

```javascript
import inquirer from 'inquirer';

// Text input
const { name } = await inquirer.prompt([
  {
    type: 'input',
    name: 'name',
    message: 'Project name:',
    default: 'my-project',
    validate: (input) => input.length > 0 || 'Name required',
  },
]);

// Select from list
const { environment } = await inquirer.prompt([
  {
    type: 'list',
    name: 'environment',
    message: 'Select environment:',
    choices: ['development', 'staging', 'production'],
    default: 'development',
  },
]);

// Checkbox (multi-select)
const { features } = await inquirer.prompt([
  {
    type: 'checkbox',
    name: 'features',
    message: 'Select features:',
    choices: [
      { name: 'TypeScript', checked: true },
      { name: 'ESLint', checked: true },
      { name: 'Prettier', checked: true },
      { name: 'Jest', checked: false },
    ],
  },
]);

// Confirmation
const { confirmed } = await inquirer.prompt([
  {
    type: 'confirm',
    name: 'confirmed',
    message: 'Deploy to production?',
    default: false,
  },
]);

// Password
const { password } = await inquirer.prompt([
  {
    type: 'password',
    name: 'password',
    message: 'Enter password:',
    mask: '*',
  },
]);
```

## Terminal Output (Chalk)

Colorful terminal output with proper TTY detection.

```javascript
import chalk from 'chalk';

// Basic colors
console.log(chalk.blue('Info: ') + 'Starting deployment...');
console.log(chalk.green('Success: ') + 'Deployment complete');
console.log(chalk.yellow('Warning: ') + 'Deprecated flag used');
console.log(chalk.red('Error: ') + 'Deployment failed');

// Styles
console.log(chalk.bold.underline('Important'));
console.log(chalk.dim('Less important'));

// Templates
const success = chalk.green.bold;
const error = chalk.red.bold;
console.log(success('✓') + ' Build successful');
console.log(error('✗') + ' Build failed');

// Disable colors for CI
const log = {
  info: (msg) => console.log(chalk.blue('ℹ'), msg),
  success: (msg) => console.log(chalk.green('✔'), msg),
  warn: (msg) => console.log(chalk.yellow('⚠'), msg),
  error: (msg) => console.log(chalk.red('✖'), msg),
};

// Auto-detects TTY and CI environments
```

## Progress Indicators (Ora)

Elegant terminal spinners and progress indicators.

```javascript
import ora from 'ora';

// Simple spinner
const spinner = ora('Loading...').start();
await doWork();
spinner.succeed('Done!');

// Update text
const spinner = ora('Starting...').start();
spinner.text = 'Processing...';
await process();
spinner.text = 'Finalizing...';
await finalize();
spinner.succeed('Complete!');

// Different states
spinner.start('Installing dependencies...');
// ... work
spinner.succeed('Dependencies installed');
// or
spinner.fail('Installation failed');
// or
spinner.warn('Some packages skipped');
// or
spinner.info('Using cached packages');

// Multiple spinners
const spinners = {
  api: ora('Deploying API...').start(),
  web: ora('Deploying web app...').start(),
  db: ora('Running migrations...').start(),
};

await Promise.all([
  deployApi().then(() => spinners.api.succeed()),
  deployWeb().then(() => spinners.web.succeed()),
  runMigrations().then(() => spinners.db.succeed()),
]);
```

## Progress Bars (cli-progress)

```javascript
import cliProgress from 'cli-progress';

// Single progress bar
const bar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
bar.start(100, 0);

for (let i = 0; i <= 100; i++) {
  await processItem(i);
  bar.update(i);
}

bar.stop();

// Multi-progress
const multibar = new cliProgress.MultiBar({
  clearOnComplete: false,
  hideCursor: true,
});

const bar1 = multibar.create(100, 0, { task: 'API' });
const bar2 = multibar.create(100, 0, { task: 'Web' });

await Promise.all([
  processApi(bar1),
  processWeb(bar2),
]);

multibar.stop();
```

## File System Helpers

```javascript
import fs from 'fs-extra';
import { globby } from 'globby';
import path from 'path';

// Copy with template
await fs.copy('templates/app', targetDir, {
  filter: (src) => !src.includes('node_modules'),
});

// Read/write JSON
const config = await fs.readJson('config.json');
await fs.writeJson('output.json', data, { spaces: 2 });

// Ensure directory exists
await fs.ensureDir('dist/assets');

// Find files
const files = await globby(['src/**/*.ts', '!src/**/*.test.ts']);
```

## Error Handling

```javascript
import { Command } from 'commander';

program
  .command('deploy')
  .action(async () => {
    try {
      await deploy();
    } catch (error) {
      if (error.code === 'EACCES') {
        console.error(chalk.red('Permission denied'));
        console.error('Try running with sudo or check file permissions');
        process.exit(77);
      } else if (error.code === 'ENOENT') {
        console.error(chalk.red('File not found:'), error.path);
        process.exit(127);
      } else {
        console.error(chalk.red('Deployment failed:'), error.message);
        if (process.env.DEBUG) {
          console.error(error.stack);
        }
        process.exit(1);
      }
    }
  });

// Handle SIGINT (Ctrl+C)
process.on('SIGINT', () => {
  console.log('\nOperation cancelled');
  process.exit(130);
});
```

## Package.json Setup

```json
{
  "name": "mycli",
  "version": "1.0.0",
  "type": "module",
  "bin": {
    "mycli": "./bin/cli.js"
  },
  "files": [
    "bin/",
    "lib/",
    "templates/"
  ],
  "engines": {
    "node": ">=18.0.0"
  },
  "dependencies": {
    "commander": "^11.0.0",
    "inquirer": "^9.0.0",
    "chalk": "^5.0.0",
    "ora": "^7.0.0"
  }
}
```

## Testing CLIs

```javascript
import { execaCommand } from 'execa';
import { describe, it, expect } from 'vitest';

describe('mycli', () => {
  it('shows version', async () => {
    const { stdout } = await execaCommand('node bin/cli.js --version');
    expect(stdout).toMatch(/\d+\.\d+\.\d+/);
  });

  it('shows help', async () => {
    const { stdout } = await execaCommand('node bin/cli.js --help');
    expect(stdout).toContain('Usage:');
  });

  it('handles invalid command', async () => {
    await expect(
      execaCommand('node bin/cli.js invalid')
    ).rejects.toThrow();
  });
});
```

---

## Reference: Python Cli

# Python CLI Development

## Typer (Recommended - Modern)

FastAPI-style CLI framework with automatic help generation.

```python
#!/usr/bin/env python3
import typer
from typing import Optional
from enum import Enum

app = typer.Typer()

class Environment(str, Enum):
    dev = "development"
    staging = "staging"
    prod = "production"

@app.command()
def init(
    name: str = typer.Argument(..., help="Project name"),
    template: str = typer.Option("default", help="Project template"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing"),
):
    """Initialize a new project"""
    typer.echo(f"Creating {name} from {template}")
    if force:
        typer.echo("Force mode enabled")

@app.command()
def deploy(
    environment: Environment = typer.Argument(..., help="Target environment"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview only"),
    config: Optional[typer.FileText] = typer.Option(None, help="Config file"),
):
    """Deploy to environment"""
    if dry_run:
        typer.echo(f"Would deploy to: {environment.value}")
    else:
        typer.echo(f"Deploying to {environment.value}...")

# Nested commands
config_app = typer.Typer()
app.add_typer(config_app, name="config", help="Manage configuration")

@config_app.command("get")
def config_get(key: str):
    """Get config value"""
    typer.echo(f"Value: {get_config(key)}")

@config_app.command("set")
def config_set(key: str, value: str):
    """Set config value"""
    set_config(key, value)
    typer.echo(f"Set {key} = {value}")

if __name__ == "__main__":
    app()
```

## Click (Widely Used)

Powerful, composable CLI framework.

```python
import click

@click.group()
@click.version_option()
def cli():
    """My awesome CLI tool"""
    pass

@cli.command()
@click.argument('name')
@click.option('--template', default='default', help='Project template')
@click.option('--force', '-f', is_flag=True, help='Overwrite existing')
def init(name, template, force):
    """Initialize a new project"""
    click.echo(f"Creating {name} from {template}")

@cli.command()
@click.argument('environment', type=click.Choice(['dev', 'staging', 'prod']))
@click.option('--dry-run', is_flag=True, help='Preview only')
@click.option('--config', type=click.File('r'), help='Config file')
def deploy(environment, dry_run, config):
    """Deploy to environment"""
    if dry_run:
        click.secho(f"Would deploy to: {environment}", fg='yellow')
    else:
        click.secho(f"Deploying to {environment}...", fg='green')

# Nested groups
@cli.group()
def config():
    """Manage configuration"""
    pass

@config.command('get')
@click.argument('key')
def config_get(key):
    """Get config value"""
    click.echo(get_config(key))

@config.command('set')
@click.argument('key')
@click.argument('value')
def config_set(key, value):
    """Set config value"""
    set_config(key, value)

if __name__ == '__main__':
    cli()
```

## Rich Terminal Output

Beautiful terminal formatting and progress indicators.

```python
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.syntax import Syntax
from rich import print as rprint

console = Console()

# Styled output
console.print("[bold blue]Info:[/] Starting deployment...")
console.print("[bold green]Success:[/] Deployment complete!")
console.print("[bold yellow]Warning:[/] Deprecated flag used")
console.print("[bold red]Error:[/] Deployment failed")

# Tables
table = Table(title="Deployments")
table.add_column("Environment", style="cyan")
table.add_column("Status", style="magenta")
table.add_column("Time", style="green")

table.add_row("Production", "✓ Success", "2m 34s")
table.add_row("Staging", "✗ Failed", "1m 12s")
console.print(table)

# Panels
console.print(Panel.fit(
    "Deploy to production?",
    title="Confirmation",
    border_style="red"
))

# Syntax highlighting
code = '''
def deploy(env: str):
    print(f"Deploying to {env}")
'''
console.print(Syntax(code, "python", theme="monokai"))

# Progress bars
with Progress() as progress:
    task = progress.add_task("[cyan]Deploying...", total=100)
    for i in range(100):
        do_work()
        progress.update(task, advance=1)

# Spinners
with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
) as progress:
    task = progress.add_task("Installing dependencies...")
    install_dependencies()
```

## Interactive Prompts (questionary)

```python
import questionary

# Text input
name = questionary.text(
    "Project name:",
    default="my-project",
    validate=lambda x: len(x) > 0 or "Name required"
).ask()

# Select from list
environment = questionary.select(
    "Select environment:",
    choices=["development", "staging", "production"],
    default="development"
).ask()

# Checkbox (multi-select)
features = questionary.checkbox(
    "Select features:",
    choices=[
        questionary.Choice("TypeScript", checked=True),
        questionary.Choice("ESLint", checked=True),
        questionary.Choice("Prettier", checked=True),
        questionary.Choice("Jest", checked=False),
    ]
).ask()

# Confirmation
confirmed = questionary.confirm(
    "Deploy to production?",
    default=False
).ask()

if confirmed:
    deploy()

# Password
password = questionary.password("Enter password:").ask()
```

## Argparse (Standard Library)

Built-in argument parsing (verbose but no dependencies).

```python
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        prog='mycli',
        description='My awesome CLI tool',
    )
    parser.add_argument('--version', action='version', version='1.0.0')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize project')
    init_parser.add_argument('name', help='Project name')
    init_parser.add_argument('--template', default='default', help='Template')
    init_parser.add_argument('-f', '--force', action='store_true')

    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy')
    deploy_parser.add_argument(
        'environment',
        choices=['dev', 'staging', 'prod'],
        help='Target environment'
    )
    deploy_parser.add_argument('--dry-run', action='store_true')
    deploy_parser.add_argument('--config', type=argparse.FileType('r'))

    args = parser.parse_args()

    if args.command == 'init':
        init(args.name, args.template, args.force)
    elif args.command == 'deploy':
        deploy(args.environment, args.dry_run, args.config)

if __name__ == '__main__':
    main()
```

## Error Handling

```python
import typer
import sys
from pathlib import Path

app = typer.Typer()

@app.command()
def deploy():
    try:
        perform_deploy()
    except PermissionError as e:
        typer.secho("Permission denied", fg=typer.colors.RED, err=True)
        typer.echo("Try running with sudo or check file permissions")
        raise typer.Exit(code=77)
    except FileNotFoundError as e:
        typer.secho(f"File not found: {e.filename}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=127)
    except Exception as e:
        typer.secho(f"Deployment failed: {e}", fg=typer.colors.RED, err=True)
        if os.getenv('DEBUG'):
            import traceback
            traceback.print_exc()
        raise typer.Exit(code=1)

# Handle KeyboardInterrupt (Ctrl+C)
def main():
    try:
        app()
    except KeyboardInterrupt:
        typer.echo("\nOperation cancelled")
        sys.exit(130)

if __name__ == "__main__":
    main()
```

## Configuration Management

```python
from pathlib import Path
from typing import Any
import json
import os

class Config:
    def __init__(self):
        self.config_paths = [
            Path("/etc/mycli/config.json"),          # System
            Path.home() / ".config" / "mycli" / "config.json",  # User
            Path.cwd() / "mycli.json",               # Project
        ]

    def load(self) -> dict[str, Any]:
        config = self._defaults()

        # Load from files (lowest to highest priority)
        for path in self.config_paths:
            if path.exists():
                with path.open() as f:
                    config.update(json.load(f))

        # Override with environment variables
        for key in config.keys():
            env_var = f"MYCLI_{key.upper()}"
            if env_var in os.environ:
                config[key] = os.environ[env_var]

        return config

    def _defaults(self) -> dict[str, Any]:
        return {
            "environment": "development",
            "verbose": False,
            "timeout": 30,
        }
```

## Setup.py / pyproject.toml

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "mycli"
version = "1.0.0"
description = "My awesome CLI tool"
requires-python = ">=3.10"
dependencies = [
    "typer[all]>=0.9.0",
    "rich>=13.0.0",
    "questionary>=2.0.0",
]

[project.scripts]
mycli = "mycli.cli:main"

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]
```

## Testing CLIs

```python
from typer.testing import CliRunner
from mycli.cli import app

runner = CliRunner()

def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "1.0.0" in result.stdout

def test_init():
    result = runner.invoke(app, ["init", "my-project"])
    assert result.exit_code == 0
    assert "Creating my-project" in result.stdout

def test_init_with_template():
    result = runner.invoke(app, ["init", "my-project", "--template", "react"])
    assert result.exit_code == 0
    assert "react" in result.stdout

def test_invalid_command():
    result = runner.invoke(app, ["invalid"])
    assert result.exit_code != 0
```

## Progress Bars (tqdm)

```python
from tqdm import tqdm
import time

# Simple progress bar
for i in tqdm(range(100), desc="Processing"):
    process_item(i)

# Custom format
with tqdm(total=100, desc="Downloading", unit="MB") as pbar:
    for chunk in download_chunks():
        pbar.update(len(chunk))

# Multiple progress bars
from tqdm import trange

for epoch in trange(10, desc="Epochs"):
    for batch in trange(100, desc="Batches", leave=False):
        train_batch(batch)
```

---

## Reference: Ux Patterns

# CLI UX Patterns

## Progress Indicators

### When to Use What

```
Determinate (known total):
  [████████████░░░░░░░░] 60% (3/5 files)
  Use: File operations, downloads, batch processing

Indeterminate (unknown duration):
  ⠋ Loading...
  Use: API calls, database queries, waiting for external services

Multi-step:
  ✓ Dependencies installed
  ⠋ Building application...
  ⏳ Running tests...
  Use: Multi-phase operations (build, deploy, etc.)
```

### Progress Bar Best Practices

```
Good:
[████████████░░░░░░░░] 60% | 120/200 MB | 2.4 MB/s | ETA: 33s
↑ Visual     ↑ Percent  ↑ Progress  ↑ Rate     ↑ Time

Components:
- Visual bar (20-40 chars)
- Percentage (when known)
- Current/total (with units)
- Speed/rate (when applicable)
- ETA (estimated time remaining)

Bad:
Processing... (no feedback)
60% (no context)
[████████████████████████████████████████] (too wide)
```

### Spinner Styles

```
⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏   Dots (elegant, low-key)
⣾ ⣽ ⣻ ⢿ ⡿ ⣟ ⣯ ⣷        Blocks (bold, attention)
◐ ◓ ◑ ◒                  Circle (classic)
▖ ▘ ▝ ▗                  Corners (minimal)
⠁ ⠂ ⠄ ⡀ ⢀ ⠠ ⠐ ⠈        Line (subtle)

Choose based on:
- Terminal compatibility (stick to ASCII for Windows)
- Branding (match your tool's personality)
- Context (subtle for background, bold for main task)
```

## Color Usage

### Semantic Colors

```
Red:     Errors, failures, destructive actions
Yellow:  Warnings, deprecations, non-critical issues
Green:   Success, completion, positive feedback
Blue:    Information, hints, neutral messages
Cyan:    Commands, code, technical details
Magenta: Highlights, special items
Gray:    Less important, metadata, timestamps

Examples:
✓ Success: Deployment complete
✗ Error: File not found
⚠ Warning: Deprecated flag --old-flag
ℹ Info: Using cache from ~/.mycli/cache
```

### When to Disable Colors

```javascript
// Detect non-TTY output (piped to file, etc.)
const noColor = !process.stdout.isTTY ||
                process.env.NO_COLOR ||
                process.env.CI === 'true';

if (noColor) {
  // Disable colors
}

// Support NO_COLOR standard
// https://no-color.org/
```

### Color Accessibility

```
- Don't rely on color alone (use symbols too)
- Provide high contrast (test with various terminals)
- Support color blindness (red/green alternatives)

Good:
✓ Build successful (green)
✗ Build failed (red)
↑ Symbols work without color

Bad:
Success (only color, no symbol)
Failed (only color, no symbol)
```

## Help Text Design

### Command Help Structure

```
USAGE
  mycli <command> [options]

COMMANDS
  init         Initialize a new project
  deploy       Deploy to environment
  config       Manage configuration
  plugins      Manage plugins

OPTIONS
  -h, --help     Show help
  -v, --version  Show version
  --config FILE  Config file path

Run 'mycli <command> --help' for more information on a command.

EXAMPLES
  # Initialize a new project
  mycli init my-app

  # Deploy to production
  mycli deploy production --dry-run

Learn more: https://docs.mycli.dev
```

### Subcommand Help

```
USAGE
  mycli deploy <environment> [options]

ARGUMENTS
  environment    Target environment (required)
                 Values: development, staging, production

OPTIONS
  -c, --config <file>    Config file path
                         Default: ./mycli.config.yml

  -f, --force            Skip confirmation prompts
                         Use with caution in production

  -d, --dry-run          Preview changes without executing
                         Shows what would happen

  -v, --verbose          Show detailed output
                         Includes debug information

EXAMPLES
  # Deploy to production (with confirmation)
  mycli deploy production

  # Preview staging deployment
  mycli deploy staging --dry-run

  # Use custom config
  mycli deploy production --config ./prod.yml

  # Force deploy without prompts
  mycli deploy production --force

For more information, visit https://docs.mycli.dev/deploy
```

## Error Messages

### Good Error Messages

```
Pattern: [Context] → [Problem] → [Solution]

Example 1: File not found
✗ Error: Config file not found

Searched locations:
  • ./mycli.config.yml
  • ~/.config/mycli/config.yml
  • /etc/mycli/config.yml

Solutions:
  • Run 'mycli init' to create a config file
  • Use --config to specify a different location
  • Check file permissions

Example 2: Validation error
✗ Error: Invalid environment 'prod'

Expected one of:
  • development
  • staging
  • production

Did you mean 'production'?

Example 3: Permission error
✗ Error: Permission denied writing to /etc/mycli/config.yml

This operation requires elevated permissions.

Try:
  • Run with sudo: sudo mycli config set key value
  • Use user config: mycli config set --user key value
  • Check file permissions: ls -la /etc/mycli/config.yml
```

### Error Message Guidelines

```
DO:
✓ Be specific ("Port 3000 already in use" not "Port unavailable")
✓ Show context ("in file config.yml, line 42")
✓ Suggest solutions ("Try running 'mycli fix'")
✓ Use plain language ("File not found" not "ENOENT")

DON'T:
✗ Show stack traces to users (save for --debug)
✗ Use jargon ("EACCES: permission denied")
✗ Leave users stuck ("Invalid input" with no explanation)
✗ Be vague ("Something went wrong")
```

## Interactive Prompts

### Prompt Types

```
Text Input:
  Project name: my-awesome-app
  ↑ Clear label

Select (Single Choice):
  ? Select environment: (Use arrow keys)
  ❯ development
    staging
    production

Checkbox (Multiple Choice):
  ? Select features: (Press space to select, enter to confirm)
  ◉ TypeScript
  ◯ ESLint
  ◉ Prettier
  ◯ Jest

Confirmation:
  ? Deploy to production? (y/N)
  ↑ Default is No (safer)

Password:
  ? Enter password: ********
  ↑ Masked input
```

### Prompt Guidelines

```
DO:
✓ Show keyboard hints ("Use arrow keys", "Press space")
✓ Provide sensible defaults (pre-select common choices)
✓ Allow skipping with Ctrl+C
✓ Validate input immediately
✓ Show preview/summary before final action

DON'T:
✗ Require interaction in CI/CD environments
✗ Ask obvious questions (confirm every action)
✗ Hide what will happen next
✗ Make users repeat information
```

## Output Formatting

### Tables

```
Good:
┌─────────────┬──────────┬──────────┐
│ Environment │ Status   │ Updated  │
├─────────────┼──────────┼──────────┤
│ production  │ ✓ Active │ 2h ago   │
│ staging     │ ✓ Active │ 5m ago   │
│ development │ ✗ Down   │ 1d ago   │
└─────────────┴──────────┴──────────┘

Minimal (for scripting):
Environment  Status  Updated
production   Active  2h ago
staging      Active  5m ago
development  Down    1d ago

JSON (for programmatic use):
[
  {"env": "production", "status": "active", "updated": "2h ago"},
  {"env": "staging", "status": "active", "updated": "5m ago"}
]
```

### Lists

```
Bulleted:
Features:
  • TypeScript support
  • Hot reload
  • Auto-formatting

Numbered:
Steps to deploy:
  1. Build application
  2. Run tests
  3. Deploy to server
  4. Verify deployment

Tree:
my-app/
├── src/
│   ├── components/
│   └── utils/
├── tests/
└── package.json
```

## Status Messages

### Real-time Updates

```
Multi-step process:
✓ Dependencies installed (2.3s)
✓ Application built (8.1s)
⠋ Running tests... (current)
⏳ Deploying... (pending)
⏳ Verifying... (pending)

Updates:
⠋ Installing dependencies...
  → npm install
✓ Dependencies installed (2.3s)

⠋ Building application...
  → webpack build
✓ Application built (8.1s)
  → Output: dist/ (2.4 MB)
```

### Summary/Completion

```
✓ Deployment complete!

Summary:
  Environment:  production
  Version:      v1.2.3
  Duration:     2m 34s
  Deployed:     2023-12-14 10:30:45 UTC

Next steps:
  • View logs: mycli logs production
  • Monitor:   mycli status production
  • Rollback:  mycli rollback production

URL: https://app.example.com
```

## Debugging & Verbose Mode

```
Normal mode (default):
✓ Deployed to production (2m 34s)

Verbose mode (--verbose):
[10:30:12] Starting deployment...
[10:30:13] Loading config from ./mycli.config.yml
[10:30:14] Connecting to production server...
[10:30:15] Uploading files (124 files, 2.4 MB)...
[10:30:28] Running post-deploy hooks...
[10:32:46] ✓ Deployment complete

Debug mode (--debug):
[DEBUG] Config loaded: {env: 'production', ...}
[DEBUG] SSH connection established: user@host
[DEBUG] Executing: rsync -avz ./dist/ user@host:/var/www/
[DEBUG] Output: sending incremental file list...
[DEBUG] Exit code: 0
✓ Deployed to production (2m 34s)

Usage:
# Normal: concise output
mycli deploy production

# Verbose: detailed steps
mycli deploy production --verbose

# Debug: everything including internals
DEBUG=* mycli deploy production
```

## Man Page Format

```
NAME
    mycli-deploy - Deploy application to environment

SYNOPSIS
    mycli deploy <environment> [options]

DESCRIPTION
    Deploy your application to the specified environment.
    Supports development, staging, and production environments.

OPTIONS
    -c, --config <file>
        Path to configuration file
        Default: ./mycli.config.yml

    -f, --force
        Skip all confirmation prompts
        Use with caution in production

    -d, --dry-run
        Preview deployment without executing
        Shows what would be deployed

EXAMPLES
    Deploy to production:
        mycli deploy production

    Preview staging deployment:
        mycli deploy staging --dry-run

SEE ALSO
    mycli-init(1), mycli-config(1), mycli-rollback(1)
```
