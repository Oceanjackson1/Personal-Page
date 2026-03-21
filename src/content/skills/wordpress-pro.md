---
title: "WordPress 专业开发"
description: "WordPress 高级开发，主题和插件开发、性能优化和安全加固"
category: "development"
source: "community"
author: "Community"
tags: ["wordpress"]
date: 2026-03-20
---

# WordPress Pro

Expert WordPress developer specializing in custom themes, plugins, Gutenberg blocks, WooCommerce, and WordPress performance optimization.

## Core Workflow

1. **Analyze requirements** — Understand WordPress context, existing setup, and goals.
2. **Design architecture** — Plan theme/plugin structure, hooks, and data flow.
3. **Implement** — Build using WordPress coding standards and security best practices.
4. **Validate** — Run `phpcs --standard=WordPress` to catch WPCS violations; verify nonce handling and capability checks manually.
5. **Optimize** — Apply transient/object caching, query optimization, and asset enqueuing.
6. **Test & secure** — Confirm sanitization/escaping on all I/O, test across target WordPress versions, and run a security audit checklist.

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Theme Development | `references/theme-development.md` | Templates, hierarchy, child themes, FSE |
| Plugin Architecture | `references/plugin-architecture.md` | Structure, activation, settings API, updates |
| Gutenberg Blocks | `references/gutenberg-blocks.md` | Block dev, patterns, FSE, dynamic blocks |
| Hooks & Filters | `references/hooks-filters.md` | Actions, filters, custom hooks, priorities |
| Performance & Security | `references/performance-security.md` | Caching, optimization, hardening, backups |

## Key Implementation Patterns

### Nonce Verification (form submissions)
```php
// Output nonce field in form
wp_nonce_field( 'my_action', 'my_nonce' );

// Verify on submission — bail early if invalid
if ( ! isset( $_POST['my_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['my_nonce'] ) ), 'my_action' ) ) {
    wp_die( esc_html__( 'Security check failed.', 'my-textdomain' ) );
}
```

### Sanitization & Escaping
```php
// Sanitize input (store)
$title   = sanitize_text_field( wp_unslash( $_POST['title'] ?? '' ) );
$content = wp_kses_post( wp_unslash( $_POST['content'] ?? '' ) );
$url     = esc_url_raw( wp_unslash( $_POST['url'] ?? '' ) );

// Escape output (display)
echo esc_html( $title );
echo wp_kses_post( $content );
echo '<a href="' . esc_url( $url ) . '">' . esc_html__( 'Link', 'my-textdomain' ) . '</a>';
```

### Enqueuing Scripts & Styles
```php
add_action( 'wp_enqueue_scripts', 'my_theme_assets' );
function my_theme_assets(): void {
    wp_enqueue_style(
        'my-theme-style',
        get_stylesheet_uri(),
        [],
        wp_get_theme()->get( 'Version' )
    );
    wp_enqueue_script(
        'my-theme-script',
        get_template_directory_uri() . '/assets/js/main.js',
        [ 'jquery' ],
        '1.0.0',
        true // load in footer
    );
    // Pass server data to JS safely
    wp_localize_script( 'my-theme-script', 'MyTheme', [
        'ajaxUrl' => admin_url( 'admin-ajax.php' ),
        'nonce'   => wp_create_nonce( 'my_ajax_nonce' ),
    ] );
}
```

### Prepared Database Queries
```php
global $wpdb;
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->prefix}my_table WHERE user_id = %d AND status = %s",
        absint( $user_id ),
        sanitize_text_field( $status )
    )
);
```

### Capability Checks
```php
// Always check capabilities before sensitive operations
if ( ! current_user_can( 'manage_options' ) ) {
    wp_die( esc_html__( 'You do not have permission to do this.', 'my-textdomain' ) );
}
```

## Constraints

### MUST DO
- Follow WordPress Coding Standards (WPCS); validate with `phpcs --standard=WordPress`
- Use nonces for all form submissions and AJAX requests
- Sanitize all user inputs with appropriate functions (`sanitize_text_field`, `wp_kses_post`, etc.)
- Escape all outputs (`esc_html`, `esc_url`, `esc_attr`, `wp_kses_post`)
- Use prepared statements for all database queries (`$wpdb->prepare`)
- Implement proper capability checks before privileged operations
- Enqueue scripts/styles via `wp_enqueue_scripts` / `admin_enqueue_scripts` hooks
- Use WordPress hooks instead of modifying core
- Write translatable strings with text domains (`__()`, `esc_html__()`, etc.)
- Test across target WordPress versions

### MUST NOT DO
- Modify WordPress core files
- Use PHP short tags or deprecated functions
- Trust user input without sanitization
- Output data without escaping
- Hardcode database table names (use `$wpdb->prefix`)
- Skip capability checks in admin functions
- Ignore SQL injection vectors
- Bundle unnecessary libraries when WordPress APIs suffice
- Allow unsafe file upload handling
- Skip internationalization (i18n)

## Output Templates

When implementing WordPress features, provide:
1. Main plugin/theme file with proper headers
2. Relevant template files or block code
3. Functions with proper WordPress hooks
4. Security implementations (nonces, sanitization, escaping)
5. Brief explanation of WordPress-specific patterns used

## Knowledge Reference

WordPress 6.4+, PHP 8.1+, Gutenberg, WooCommerce, ACF, REST API, WP-CLI, block development, theme customizer, widget API, shortcode API, transients, object caching, query optimization, security hardening, WPCS

---

## Reference: Gutenberg Blocks

# Gutenberg Blocks

---

## Block Development Overview

WordPress 6.4+ uses the Block Editor (Gutenberg) as the primary editing experience. Blocks are the fundamental building units.

### Block Types

| Type | Description | Use Case |
|------|-------------|----------|
| Static | Fixed HTML output | Simple content, images |
| Dynamic | Server-rendered | Posts list, dynamic data |
| Interactive | Client-side JS | Accordions, tabs, carousels |

---

## Project Setup

### Using @wordpress/create-block

```bash
# Create a new block plugin
npx @wordpress/create-block my-block --namespace my-plugin

# Create with specific template
npx @wordpress/create-block my-block --template @wordpress/create-block-interactive-template

# Create dynamic block
npx @wordpress/create-block my-block --variant dynamic
```

### Generated Structure

```
my-block/
├── my-block.php           # Plugin file
├── package.json           # NPM dependencies
├── src/
│   ├── block.json         # Block metadata
│   ├── edit.js            # Editor component
│   ├── save.js            # Frontend save
│   ├── index.js           # Block registration
│   ├── editor.scss        # Editor styles
│   └── style.scss         # Frontend styles
├── build/                 # Compiled assets
└── readme.txt
```

### package.json Scripts

```json
{
    "name": "my-block",
    "version": "1.0.0",
    "scripts": {
        "build": "wp-scripts build",
        "start": "wp-scripts start",
        "format": "wp-scripts format",
        "lint:js": "wp-scripts lint-js",
        "lint:css": "wp-scripts lint-style",
        "packages-update": "wp-scripts packages-update"
    },
    "devDependencies": {
        "@wordpress/scripts": "^27.0.0"
    }
}
```

---

## Block Registration

### block.json (WordPress 6.4+)

```json
{
    "$schema": "https://schemas.wp.org/trunk/block.json",
    "apiVersion": 3,
    "name": "my-plugin/my-block",
    "version": "1.0.0",
    "title": "My Block",
    "category": "widgets",
    "icon": "smiley",
    "description": "A custom block for displaying content.",
    "keywords": ["custom", "content", "block"],
    "supports": {
        "html": false,
        "align": ["wide", "full"],
        "anchor": true,
        "color": {
            "background": true,
            "text": true,
            "link": true,
            "gradients": true
        },
        "spacing": {
            "margin": true,
            "padding": true,
            "blockGap": true
        },
        "typography": {
            "fontSize": true,
            "lineHeight": true
        },
        "__experimentalBorder": {
            "color": true,
            "radius": true,
            "style": true,
            "width": true
        }
    },
    "attributes": {
        "content": {
            "type": "string",
            "source": "html",
            "selector": "p"
        },
        "alignment": {
            "type": "string",
            "default": "left"
        },
        "showBorder": {
            "type": "boolean",
            "default": false
        },
        "items": {
            "type": "array",
            "default": []
        },
        "selectedPostId": {
            "type": "number"
        }
    },
    "example": {
        "attributes": {
            "content": "Example content for the block preview."
        }
    },
    "textdomain": "my-plugin",
    "editorScript": "file:./index.js",
    "editorStyle": "file:./index.css",
    "style": "file:./style-index.css",
    "viewScript": "file:./view.js",
    "render": "file:./render.php"
}
```

### PHP Registration

```php
<?php
declare(strict_types=1);

/**
 * Register all blocks
 */
function my_plugin_register_blocks(): void {
    // Auto-register from block.json
    register_block_type(__DIR__ . '/build/my-block');

    // Or with additional arguments
    register_block_type(__DIR__ . '/build/another-block', [
        'render_callback' => 'my_plugin_render_another_block',
    ]);
}
add_action('init', 'my_plugin_register_blocks');

/**
 * Register block category
 */
function my_plugin_block_categories(array $categories): array {
    return array_merge(
        [
            [
                'slug'  => 'my-plugin-blocks',
                'title' => __('My Plugin Blocks', 'my-plugin'),
                'icon'  => 'wordpress',
            ],
        ],
        $categories
    );
}
add_filter('block_categories_all', 'my_plugin_block_categories');
```

---

## Static Block Development

### index.js (Entry Point)

```javascript
/**
 * WordPress dependencies
 */
import { registerBlockType } from '@wordpress/blocks';

/**
 * Internal dependencies
 */
import Edit from './edit';
import save from './save';
import metadata from './block.json';
import './style.scss';

/**
 * Register block
 */
registerBlockType(metadata.name, {
    edit: Edit,
    save,
});
```

### edit.js (Editor Component)

```javascript
/**
 * WordPress dependencies
 */
import { __ } from '@wordpress/i18n';
import {
    useBlockProps,
    RichText,
    InspectorControls,
    BlockControls,
    AlignmentToolbar,
    MediaUpload,
    MediaUploadCheck,
} from '@wordpress/block-editor';
import {
    PanelBody,
    ToggleControl,
    TextControl,
    SelectControl,
    RangeControl,
    Button,
} from '@wordpress/components';
import './editor.scss';

/**
 * Edit component
 *
 * @param {Object} props               Block props
 * @param {Object} props.attributes    Block attributes
 * @param {Function} props.setAttributes Function to update attributes
 * @return {JSX.Element} Block edit component
 */
export default function Edit({ attributes, setAttributes }) {
    const { content, alignment, showBorder, imageId, imageUrl, columns } = attributes;

    const blockProps = useBlockProps({
        className: `align-${alignment}${showBorder ? ' has-border' : ''}`,
    });

    const onSelectImage = (media) => {
        setAttributes({
            imageId: media.id,
            imageUrl: media.url,
        });
    };

    const onRemoveImage = () => {
        setAttributes({
            imageId: undefined,
            imageUrl: undefined,
        });
    };

    return (
        <>
            <BlockControls>
                <AlignmentToolbar
                    value={alignment}
                    onChange={(newAlignment) =>
                        setAttributes({ alignment: newAlignment })
                    }
                />
            </BlockControls>

            <InspectorControls>
                <PanelBody title={__('Settings', 'my-plugin')} initialOpen={true}>
                    <ToggleControl
                        label={__('Show Border', 'my-plugin')}
                        checked={showBorder}
                        onChange={(value) => setAttributes({ showBorder: value })}
                    />

                    <RangeControl
                        label={__('Columns', 'my-plugin')}
                        value={columns}
                        onChange={(value) => setAttributes({ columns: value })}
                        min={1}
                        max={6}
                    />

                    <SelectControl
                        label={__('Layout', 'my-plugin')}
                        value={attributes.layout}
                        options={[
                            { label: __('Default', 'my-plugin'), value: 'default' },
                            { label: __('Card', 'my-plugin'), value: 'card' },
                            { label: __('Minimal', 'my-plugin'), value: 'minimal' },
                        ]}
                        onChange={(value) => setAttributes({ layout: value })}
                    />
                </PanelBody>

                <PanelBody title={__('Image', 'my-plugin')} initialOpen={false}>
                    <MediaUploadCheck>
                        <MediaUpload
                            onSelect={onSelectImage}
                            allowedTypes={['image']}
                            value={imageId}
                            render={({ open }) => (
                                <div className="editor-post-featured-image">
                                    {imageUrl ? (
                                        <>
                                            <img src={imageUrl} alt="" />
                                            <Button
                                                onClick={onRemoveImage}
                                                isDestructive
                                            >
                                                {__('Remove Image', 'my-plugin')}
                                            </Button>
                                        </>
                                    ) : (
                                        <Button onClick={open} variant="secondary">
                                            {__('Select Image', 'my-plugin')}
                                        </Button>
                                    )}
                                </div>
                            )}
                        />
                    </MediaUploadCheck>
                </PanelBody>
            </InspectorControls>

            <div {...blockProps}>
                {imageUrl && (
                    <img src={imageUrl} alt="" className="block-image" />
                )}
                <RichText
                    tagName="p"
                    value={content}
                    onChange={(value) => setAttributes({ content: value })}
                    placeholder={__('Enter content...', 'my-plugin')}
                    allowedFormats={['core/bold', 'core/italic', 'core/link']}
                />
            </div>
        </>
    );
}
```

### save.js (Frontend Output)

```javascript
/**
 * WordPress dependencies
 */
import { useBlockProps, RichText } from '@wordpress/block-editor';

/**
 * Save component
 *
 * @param {Object} props            Block props
 * @param {Object} props.attributes Block attributes
 * @return {JSX.Element} Block save component
 */
export default function save({ attributes }) {
    const { content, alignment, showBorder, imageUrl } = attributes;

    const blockProps = useBlockProps.save({
        className: `align-${alignment}${showBorder ? ' has-border' : ''}`,
    });

    return (
        <div {...blockProps}>
            {imageUrl && (
                <img src={imageUrl} alt="" className="block-image" />
            )}
            <RichText.Content tagName="p" value={content} />
        </div>
    );
}
```

---

## Dynamic Block Development

Dynamic blocks render on the server, useful for content that changes or requires PHP logic.

### block.json for Dynamic Block

```json
{
    "$schema": "https://schemas.wp.org/trunk/block.json",
    "apiVersion": 3,
    "name": "my-plugin/recent-posts",
    "title": "Recent Posts",
    "category": "widgets",
    "icon": "list-view",
    "description": "Display recent posts with customizable options.",
    "supports": {
        "html": false,
        "align": ["wide", "full"]
    },
    "attributes": {
        "numberOfPosts": {
            "type": "number",
            "default": 5
        },
        "postType": {
            "type": "string",
            "default": "post"
        },
        "showExcerpt": {
            "type": "boolean",
            "default": true
        },
        "showFeaturedImage": {
            "type": "boolean",
            "default": true
        },
        "categories": {
            "type": "array",
            "default": []
        }
    },
    "textdomain": "my-plugin",
    "editorScript": "file:./index.js",
    "style": "file:./style-index.css",
    "render": "file:./render.php"
}
```

### edit.js for Dynamic Block

```javascript
/**
 * WordPress dependencies
 */
import { __ } from '@wordpress/i18n';
import { useBlockProps, InspectorControls } from '@wordpress/block-editor';
import {
    PanelBody,
    RangeControl,
    ToggleControl,
    SelectControl,
    Spinner,
} from '@wordpress/components';
import { useSelect } from '@wordpress/data';
import { store as coreStore } from '@wordpress/core-data';
import ServerSideRender from '@wordpress/server-side-render';

/**
 * Edit component for dynamic block
 */
export default function Edit({ attributes, setAttributes }) {
    const { numberOfPosts, postType, showExcerpt, showFeaturedImage } = attributes;

    const blockProps = useBlockProps();

    // Fetch post types for select
    const postTypes = useSelect((select) => {
        const { getPostTypes } = select(coreStore);
        const types = getPostTypes({ per_page: -1 });
        return types?.filter((type) => type.viewable && type.rest_base) || [];
    }, []);

    // Fetch categories
    const categories = useSelect((select) => {
        const { getEntityRecords } = select(coreStore);
        return getEntityRecords('taxonomy', 'category', { per_page: -1 }) || [];
    }, []);

    const postTypeOptions = postTypes.map((type) => ({
        label: type.labels.singular_name,
        value: type.slug,
    }));

    return (
        <>
            <InspectorControls>
                <PanelBody title={__('Settings', 'my-plugin')}>
                    <RangeControl
                        label={__('Number of Posts', 'my-plugin')}
                        value={numberOfPosts}
                        onChange={(value) => setAttributes({ numberOfPosts: value })}
                        min={1}
                        max={20}
                    />

                    {postTypeOptions.length > 0 && (
                        <SelectControl
                            label={__('Post Type', 'my-plugin')}
                            value={postType}
                            options={postTypeOptions}
                            onChange={(value) => setAttributes({ postType: value })}
                        />
                    )}

                    <ToggleControl
                        label={__('Show Excerpt', 'my-plugin')}
                        checked={showExcerpt}
                        onChange={(value) => setAttributes({ showExcerpt: value })}
                    />

                    <ToggleControl
                        label={__('Show Featured Image', 'my-plugin')}
                        checked={showFeaturedImage}
                        onChange={(value) => setAttributes({ showFeaturedImage: value })}
                    />
                </PanelBody>
            </InspectorControls>

            <div {...blockProps}>
                <ServerSideRender
                    block="my-plugin/recent-posts"
                    attributes={attributes}
                    LoadingResponsePlaceholder={() => (
                        <div className="loading-placeholder">
                            <Spinner />
                            <p>{__('Loading...', 'my-plugin')}</p>
                        </div>
                    )}
                    EmptyResponsePlaceholder={() => (
                        <p>{__('No posts found.', 'my-plugin')}</p>
                    )}
                />
            </div>
        </>
    );
}
```

### render.php (Server-Side Render)

```php
<?php
/**
 * Server-side rendering for Recent Posts block
 *
 * @var array    $attributes Block attributes
 * @var string   $content    Block content
 * @var WP_Block $block      Block instance
 */

declare(strict_types=1);

defined('ABSPATH') || exit;

$number_of_posts = absint($attributes['numberOfPosts'] ?? 5);
$post_type = sanitize_key($attributes['postType'] ?? 'post');
$show_excerpt = (bool) ($attributes['showExcerpt'] ?? true);
$show_featured_image = (bool) ($attributes['showFeaturedImage'] ?? true);
$categories = array_map('absint', $attributes['categories'] ?? []);

$query_args = [
    'post_type'      => $post_type,
    'posts_per_page' => $number_of_posts,
    'post_status'    => 'publish',
    'orderby'        => 'date',
    'order'          => 'DESC',
];

if (!empty($categories) && $post_type === 'post') {
    $query_args['category__in'] = $categories;
}

$posts_query = new WP_Query($query_args);

$wrapper_attributes = get_block_wrapper_attributes([
    'class' => 'recent-posts-block',
]);
?>

<div <?php echo $wrapper_attributes; ?>>
    <?php if ($posts_query->have_posts()) : ?>
        <ul class="recent-posts-list">
            <?php while ($posts_query->have_posts()) : $posts_query->the_post(); ?>
                <li class="recent-posts-item">
                    <?php if ($show_featured_image && has_post_thumbnail()) : ?>
                        <div class="post-thumbnail">
                            <a href="<?php the_permalink(); ?>">
                                <?php the_post_thumbnail('thumbnail'); ?>
                            </a>
                        </div>
                    <?php endif; ?>

                    <div class="post-content">
                        <h3 class="post-title">
                            <a href="<?php the_permalink(); ?>">
                                <?php the_title(); ?>
                            </a>
                        </h3>

                        <time class="post-date" datetime="<?php echo esc_attr(get_the_date('c')); ?>">
                            <?php echo esc_html(get_the_date()); ?>
                        </time>

                        <?php if ($show_excerpt) : ?>
                            <div class="post-excerpt">
                                <?php the_excerpt(); ?>
                            </div>
                        <?php endif; ?>
                    </div>
                </li>
            <?php endwhile; ?>
        </ul>
    <?php else : ?>
        <p class="no-posts"><?php esc_html_e('No posts found.', 'my-plugin'); ?></p>
    <?php endif; ?>

    <?php wp_reset_postdata(); ?>
</div>
```

---

## Block Patterns

### Registering Patterns in PHP

```php
<?php
/**
 * Register block patterns
 */
function my_plugin_register_patterns(): void {
    // Register pattern category
    register_block_pattern_category('my-plugin-patterns', [
        'label' => __('My Plugin Patterns', 'my-plugin'),
    ]);

    // Register pattern
    register_block_pattern('my-plugin/hero-section', [
        'title'       => __('Hero Section', 'my-plugin'),
        'description' => __('A full-width hero section with heading and CTA.', 'my-plugin'),
        'categories'  => ['my-plugin-patterns', 'featured'],
        'keywords'    => ['hero', 'banner', 'cta'],
        'blockTypes'  => ['core/template-part/header'],
        'content'     => '<!-- wp:cover {"dimRatio":60,"overlayColor":"black","align":"full"} -->
            <div class="wp-block-cover alignfull">
                <span class="wp-block-cover__background has-black-background-color has-background-dim-60"></span>
                <div class="wp-block-cover__inner-container">
                    <!-- wp:heading {"textAlign":"center","level":1} -->
                    <h1 class="wp-block-heading has-text-align-center">' . esc_html__('Welcome', 'my-plugin') . '</h1>
                    <!-- /wp:heading -->
                    <!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
                    <div class="wp-block-buttons">
                        <!-- wp:button -->
                        <div class="wp-block-button"><a class="wp-block-button__link wp-element-button">' . esc_html__('Get Started', 'my-plugin') . '</a></div>
                        <!-- /wp:button -->
                    </div>
                    <!-- /wp:buttons -->
                </div>
            </div>
            <!-- /wp:cover -->',
    ]);
}
add_action('init', 'my_plugin_register_patterns');
```

### Pattern File (patterns/feature-grid.php)

```php
<?php
/**
 * Title: Feature Grid
 * Slug: my-plugin/feature-grid
 * Categories: my-plugin-patterns
 * Keywords: features, grid, cards
 * Block Types: core/group
 * Viewport Width: 1200
 */

declare(strict_types=1);

defined('ABSPATH') || exit;
?>

<!-- wp:group {"align":"wide","layout":{"type":"constrained"}} -->
<div class="wp-block-group alignwide">
    <!-- wp:heading {"textAlign":"center"} -->
    <h2 class="wp-block-heading has-text-align-center"><?php esc_html_e('Our Features', 'my-plugin'); ?></h2>
    <!-- /wp:heading -->

    <!-- wp:columns {"align":"wide"} -->
    <div class="wp-block-columns alignwide">
        <!-- wp:column -->
        <div class="wp-block-column">
            <!-- wp:group {"style":{"spacing":{"padding":{"top":"var:preset|spacing|m","right":"var:preset|spacing|m","bottom":"var:preset|spacing|m","left":"var:preset|spacing|m"}},"border":{"radius":"8px"}},"backgroundColor":"base-alt"} -->
            <div class="wp-block-group has-base-alt-background-color has-background">
                <!-- wp:image {"width":"64px","sizeSlug":"full"} -->
                <figure class="wp-block-image size-full is-resized" style="width:64px"><img src="<?php echo esc_url(get_template_directory_uri()); ?>/assets/images/icon-feature-1.svg" alt="" /></figure>
                <!-- /wp:image -->
                <!-- wp:heading {"level":3} -->
                <h3 class="wp-block-heading"><?php esc_html_e('Feature One', 'my-plugin'); ?></h3>
                <!-- /wp:heading -->
                <!-- wp:paragraph -->
                <p><?php esc_html_e('Description of the first feature goes here.', 'my-plugin'); ?></p>
                <!-- /wp:paragraph -->
            </div>
            <!-- /wp:group -->
        </div>
        <!-- /wp:column -->

        <!-- wp:column -->
        <div class="wp-block-column">
            <!-- wp:group {"style":{"spacing":{"padding":{"top":"var:preset|spacing|m","right":"var:preset|spacing|m","bottom":"var:preset|spacing|m","left":"var:preset|spacing|m"}},"border":{"radius":"8px"}},"backgroundColor":"base-alt"} -->
            <div class="wp-block-group has-base-alt-background-color has-background">
                <!-- wp:image {"width":"64px","sizeSlug":"full"} -->
                <figure class="wp-block-image size-full is-resized" style="width:64px"><img src="<?php echo esc_url(get_template_directory_uri()); ?>/assets/images/icon-feature-2.svg" alt="" /></figure>
                <!-- /wp:image -->
                <!-- wp:heading {"level":3} -->
                <h3 class="wp-block-heading"><?php esc_html_e('Feature Two', 'my-plugin'); ?></h3>
                <!-- /wp:heading -->
                <!-- wp:paragraph -->
                <p><?php esc_html_e('Description of the second feature goes here.', 'my-plugin'); ?></p>
                <!-- /wp:paragraph -->
            </div>
            <!-- /wp:group -->
        </div>
        <!-- /wp:column -->

        <!-- wp:column -->
        <div class="wp-block-column">
            <!-- wp:group {"style":{"spacing":{"padding":{"top":"var:preset|spacing|m","right":"var:preset|spacing|m","bottom":"var:preset|spacing|m","left":"var:preset|spacing|m"}},"border":{"radius":"8px"}},"backgroundColor":"base-alt"} -->
            <div class="wp-block-group has-base-alt-background-color has-background">
                <!-- wp:image {"width":"64px","sizeSlug":"full"} -->
                <figure class="wp-block-image size-full is-resized" style="width:64px"><img src="<?php echo esc_url(get_template_directory_uri()); ?>/assets/images/icon-feature-3.svg" alt="" /></figure>
                <!-- /wp:image -->
                <!-- wp:heading {"level":3} -->
                <h3 class="wp-block-heading"><?php esc_html_e('Feature Three', 'my-plugin'); ?></h3>
                <!-- /wp:heading -->
                <!-- wp:paragraph -->
                <p><?php esc_html_e('Description of the third feature goes here.', 'my-plugin'); ?></p>
                <!-- /wp:paragraph -->
            </div>
            <!-- /wp:group -->
        </div>
        <!-- /wp:column -->
    </div>
    <!-- /wp:columns -->
</div>
<!-- /wp:group -->
```

---

## Interactivity API (WordPress 6.5+)

For client-side interactivity without custom JavaScript build processes.

### Interactive Block Example

```json
{
    "$schema": "https://schemas.wp.org/trunk/block.json",
    "apiVersion": 3,
    "name": "my-plugin/counter",
    "title": "Interactive Counter",
    "supports": {
        "interactivity": true
    },
    "textdomain": "my-plugin",
    "editorScript": "file:./index.js",
    "viewScriptModule": "file:./view.js",
    "render": "file:./render.php"
}
```

### render.php with Interactivity

```php
<?php
/**
 * Interactive counter block render
 */

declare(strict_types=1);

$initial_count = absint($attributes['initialCount'] ?? 0);

wp_interactivity_state('my-plugin/counter', [
    'count' => $initial_count,
]);
?>

<div
    <?php echo get_block_wrapper_attributes(); ?>
    data-wp-interactive="my-plugin/counter"
>
    <button
        data-wp-on--click="actions.decrement"
        data-wp-bind--disabled="!state.canDecrement"
    >
        -
    </button>

    <span data-wp-text="state.count"></span>

    <button data-wp-on--click="actions.increment">
        +
    </button>
</div>
```

### view.js (Interactivity Store)

```javascript
/**
 * WordPress dependencies
 */
import { store, getContext } from '@wordpress/interactivity';

store('my-plugin/counter', {
    state: {
        get canDecrement() {
            const { count } = store('my-plugin/counter').state;
            return count > 0;
        },
    },
    actions: {
        increment() {
            const state = store('my-plugin/counter').state;
            state.count++;
        },
        decrement() {
            const state = store('my-plugin/counter').state;
            if (state.count > 0) {
                state.count--;
            }
        },
    },
});
```

---

## Best Practices

### Do

- Use `block.json` for all block metadata (API version 3)
- Leverage `useBlockProps` for proper block wrapper handling
- Use `InspectorControls` for sidebar settings
- Implement `example` in block.json for previews
- Use `ServerSideRender` for dynamic block previews
- Follow WordPress Coding Standards for PHP render callbacks
- Use CSS custom properties from theme.json
- Test blocks in isolation and within posts
- Support align wide/full when appropriate
- Use the Interactivity API for simple client-side logic

### Do Not

- Skip the `$schema` property in block.json
- Use deprecated block API versions (use apiVersion 3)
- Forget to escape output in render.php
- Hardcode styles (use theme.json presets)
- Create unnecessary server requests in edit components
- Ignore block validation warnings
- Skip internationalization for text strings
- Bundle React/WordPress packages (use externals)

---

## Reference: Hooks Filters

# Hooks & Filters

---

## WordPress Hook System

WordPress uses an event-driven architecture with two types of hooks:

| Hook Type | Purpose | Function |
|-----------|---------|----------|
| **Actions** | Execute code at specific points | `add_action()` / `do_action()` |
| **Filters** | Modify data before it's used | `add_filter()` / `apply_filters()` |

---

## Actions

Actions allow you to execute custom code at specific points in WordPress execution.

### Action Basics

```php
<?php
declare(strict_types=1);

/**
 * Register an action hook
 *
 * @param string   $hook_name     The name of the action
 * @param callable $callback      Function to execute
 * @param int      $priority      Order of execution (default: 10)
 * @param int      $accepted_args Number of arguments passed (default: 1)
 */
add_action('init', 'my_plugin_init', 10, 1);

/**
 * Execute custom code on init
 */
function my_plugin_init(): void {
    // Your code here
    register_post_type('product', [...]);
}

// Using anonymous functions (PHP 8.1+)
add_action('wp_footer', function(): void {
    echo '<!-- Custom footer content -->';
}, 99);

// Using class methods
class My_Plugin {
    public function __construct() {
        add_action('init', [$this, 'init']);
        add_action('admin_init', [$this, 'admin_init']);
    }

    public function init(): void {
        // Initialization code
    }

    public function admin_init(): void {
        // Admin initialization
    }
}

// Using static methods
add_action('init', [My_Plugin::class, 'static_init']);
```

### Essential Action Hooks

```php
<?php
/**
 * Execution order and common action hooks
 */

// === EARLY LOADING ===

// After WordPress loads but before headers sent
add_action('muplugins_loaded', function(): void {
    // Must-use plugins loaded
});

// After active plugins loaded
add_action('plugins_loaded', function(): void {
    // Safe to check for other plugins
    if (class_exists('WooCommerce')) {
        // WooCommerce is active
    }
});

// After theme functions.php loaded
add_action('after_setup_theme', function(): void {
    // Theme setup: add_theme_support, register_nav_menus, etc.
}, 10);

// === MAIN INITIALIZATION ===

// WordPress fully loaded, safe for most operations
add_action('init', function(): void {
    // Register post types, taxonomies, shortcodes
    // Load text domains
    // Start session if needed
}, 10);

// All widgets registered
add_action('widgets_init', function(): void {
    // Register widget areas
    register_sidebar([...]);
});

// === ADMIN HOOKS ===

// Admin area initializing
add_action('admin_init', function(): void {
    // Register settings, add capabilities
});

// Build admin menu
add_action('admin_menu', function(): void {
    // Add menu pages
    add_menu_page(...);
});

// Enqueue admin assets
add_action('admin_enqueue_scripts', function(string $hook_suffix): void {
    // $hook_suffix: e.g., 'post.php', 'settings_page_my-settings'
    if ($hook_suffix !== 'settings_page_my-settings') {
        return;
    }
    wp_enqueue_script('my-admin-script', ...);
}, 10, 1);

// === FRONTEND HOOKS ===

// Main query parsed, before template loaded
add_action('template_redirect', function(): void {
    // Check conditions, redirect if needed
    if (is_page('restricted') && !is_user_logged_in()) {
        wp_redirect(wp_login_url());
        exit;
    }
});

// Enqueue frontend assets
add_action('wp_enqueue_scripts', function(): void {
    wp_enqueue_style('my-style', ...);
    wp_enqueue_script('my-script', ...);
});

// Inside <head> tag
add_action('wp_head', function(): void {
    // Meta tags, inline styles
    echo '<meta name="custom" content="value" />';
}, 1); // Priority 1 = early in head

// Before </body> tag
add_action('wp_footer', function(): void {
    // Tracking scripts, modals
}, 99); // Priority 99 = late in footer

// === POST/PAGE HOOKS ===

// Before post is saved
add_action('pre_post_update', function(int $post_id, array $data): void {
    // Validate or modify before save
}, 10, 2);

// After post is saved (any status)
add_action('save_post', function(int $post_id, WP_Post $post, bool $update): void {
    // Skip autosaves
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return;
    }

    // Skip revisions
    if (wp_is_post_revision($post_id)) {
        return;
    }

    // Skip specific post types
    if ($post->post_type !== 'my_post_type') {
        return;
    }

    // Update meta, trigger notifications, etc.
    update_post_meta($post_id, '_custom_meta', sanitize_text_field($_POST['custom_field'] ?? ''));
}, 10, 3);

// Post status transitions
add_action('transition_post_status', function(string $new_status, string $old_status, WP_Post $post): void {
    if ($new_status === 'publish' && $old_status !== 'publish') {
        // Post just published
        my_notify_subscribers($post);
    }
}, 10, 3);

// Post deleted (moved to trash)
add_action('wp_trash_post', function(int $post_id): void {
    // Clean up related data
});

// Post permanently deleted
add_action('before_delete_post', function(int $post_id, WP_Post $post): void {
    // Clean up custom tables, files, etc.
    global $wpdb;
    $wpdb->delete(
        $wpdb->prefix . 'my_table',
        ['post_id' => $post_id],
        ['%d']
    );
}, 10, 2);

// === USER HOOKS ===

// User registered
add_action('user_register', function(int $user_id, array $userdata): void {
    // Set default meta, send welcome email
    update_user_meta($user_id, 'welcome_dismissed', false);
}, 10, 2);

// User logged in
add_action('wp_login', function(string $user_login, WP_User $user): void {
    // Log login, update last login time
    update_user_meta($user->ID, 'last_login', current_time('mysql'));
}, 10, 2);

// User logged out
add_action('wp_logout', function(int $user_id): void {
    // Cleanup session data
}, 10, 1);

// === REST API HOOKS ===

// Register REST routes
add_action('rest_api_init', function(): void {
    register_rest_route('my-plugin/v1', '/items', [
        'methods'             => 'GET',
        'callback'            => 'my_plugin_get_items',
        'permission_callback' => '__return_true',
    ]);
});

// === CRON HOOKS ===

// Schedule custom cron event
add_action('init', function(): void {
    if (!wp_next_scheduled('my_plugin_daily_task')) {
        wp_schedule_event(time(), 'daily', 'my_plugin_daily_task');
    }
});

// Handle cron event
add_action('my_plugin_daily_task', function(): void {
    // Cleanup, sync, report generation, etc.
});
```

### Removing Actions

```php
<?php
/**
 * Remove actions added by WordPress or other plugins
 */

// Remove default WordPress actions
remove_action('wp_head', 'wp_generator');
remove_action('wp_head', 'wlwmanifest_link');
remove_action('wp_head', 'rsd_link');
remove_action('wp_head', 'wp_shortlink_wp_head');
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');

// Remove action from a class (must match exact instance)
// If original: add_action('init', [$instance, 'method'], 10);
// Need to access same $instance to remove

// Remove using class name for static methods
remove_action('init', [Some_Class::class, 'static_method'], 10);

// Remove all callbacks from a hook
remove_all_actions('some_hook');

// Check if action is hooked
if (has_action('init', 'some_callback')) {
    // Callback is registered
}
```

---

## Filters

Filters modify data before it's used or displayed.

### Filter Basics

```php
<?php
declare(strict_types=1);

/**
 * Register a filter hook
 *
 * @param string   $hook_name     The name of the filter
 * @param callable $callback      Function to filter data
 * @param int      $priority      Order of execution (default: 10)
 * @param int      $accepted_args Number of arguments passed (default: 1)
 */
add_filter('the_content', 'my_plugin_modify_content', 10, 1);

/**
 * Modify post content
 *
 * @param string $content The post content
 * @return string Modified content
 */
function my_plugin_modify_content(string $content): string {
    // Always return the filtered value
    if (is_single() && in_the_loop()) {
        $content .= '<div class="post-cta">Subscribe for more!</div>';
    }
    return $content;
}

// Filter with multiple arguments
add_filter('post_thumbnail_html', function(
    string $html,
    int $post_id,
    int $thumbnail_id,
    string $size,
    string $attr
): string {
    // Add lazy loading
    return str_replace('<img', '<img loading="lazy"', $html);
}, 10, 5);
```

### Essential Filter Hooks

```php
<?php
/**
 * Common filter hooks
 */

// === CONTENT FILTERS ===

// Modify post title
add_filter('the_title', function(string $title, int $post_id): string {
    if (is_admin()) {
        return $title;
    }
    // Add icon for featured posts
    if (get_post_meta($post_id, '_is_featured', true)) {
        $title = '&#9733; ' . $title;
    }
    return $title;
}, 10, 2);

// Modify post content
add_filter('the_content', function(string $content): string {
    // Add social sharing after content
    if (is_singular('post') && in_the_loop() && is_main_query()) {
        $content .= my_plugin_get_share_buttons();
    }
    return $content;
});

// Modify excerpt length
add_filter('excerpt_length', function(int $length): int {
    return 30; // words
});

// Modify excerpt "more" text
add_filter('excerpt_more', function(string $more): string {
    return '&hellip; <a href="' . esc_url(get_permalink()) . '">Read more</a>';
});

// === QUERY FILTERS ===

// Modify main query
add_filter('pre_get_posts', function(WP_Query $query): void {
    if (is_admin() || !$query->is_main_query()) {
        return;
    }

    // Exclude category from blog
    if ($query->is_home()) {
        $query->set('cat', '-5'); // Exclude category ID 5
    }

    // Custom archive ordering
    if ($query->is_post_type_archive('product')) {
        $query->set('orderby', 'menu_order');
        $query->set('order', 'ASC');
    }
});

// Modify search results
add_filter('posts_search', function(string $search, WP_Query $query): string {
    if (!$query->is_search() || !$query->is_main_query()) {
        return $search;
    }
    // Customize search SQL
    return $search;
}, 10, 2);

// === TEMPLATE FILTERS ===

// Override template file
add_filter('template_include', function(string $template): string {
    if (is_singular('product')) {
        $custom = locate_template('templates/single-product.php');
        if ($custom) {
            return $custom;
        }
    }
    return $template;
});

// Add body classes
add_filter('body_class', function(array $classes): array {
    if (is_user_logged_in()) {
        $classes[] = 'logged-in-user';
    }
    if (wp_is_mobile()) {
        $classes[] = 'is-mobile';
    }
    return $classes;
});

// Add post classes
add_filter('post_class', function(array $classes, array $class, int $post_id): array {
    if (has_post_thumbnail($post_id)) {
        $classes[] = 'has-thumbnail';
    }
    return $classes;
}, 10, 3);

// === ADMIN FILTERS ===

// Modify admin columns
add_filter('manage_product_posts_columns', function(array $columns): array {
    $new_columns = [];
    foreach ($columns as $key => $value) {
        $new_columns[$key] = $value;
        if ($key === 'title') {
            $new_columns['price'] = __('Price', 'my-plugin');
            $new_columns['sku'] = __('SKU', 'my-plugin');
        }
    }
    return $new_columns;
});

// Populate custom columns
add_action('manage_product_posts_custom_column', function(string $column, int $post_id): void {
    switch ($column) {
        case 'price':
            echo esc_html(get_post_meta($post_id, '_price', true));
            break;
        case 'sku':
            echo esc_html(get_post_meta($post_id, '_sku', true));
            break;
    }
}, 10, 2);

// Make columns sortable
add_filter('manage_edit-product_sortable_columns', function(array $columns): array {
    $columns['price'] = 'price';
    $columns['sku'] = 'sku';
    return $columns;
});

// === URL/LINK FILTERS ===

// Modify permalink structure
add_filter('post_type_link', function(string $permalink, WP_Post $post): string {
    if ($post->post_type !== 'product') {
        return $permalink;
    }
    // Add category to permalink
    $terms = get_the_terms($post->ID, 'product_category');
    if ($terms && !is_wp_error($terms)) {
        $permalink = str_replace('%product_category%', $terms[0]->slug, $permalink);
    }
    return $permalink;
}, 10, 2);

// Modify upload directory
add_filter('upload_dir', function(array $uploads): array {
    // Custom upload path for specific post types
    if (isset($_POST['post_id'])) {
        $post_type = get_post_type((int) $_POST['post_id']);
        if ($post_type === 'product') {
            $uploads['subdir'] = '/products' . $uploads['subdir'];
            $uploads['path'] = $uploads['basedir'] . $uploads['subdir'];
            $uploads['url'] = $uploads['baseurl'] . $uploads['subdir'];
        }
    }
    return $uploads;
});

// === SECURITY FILTERS ===

// Modify allowed HTML in wp_kses
add_filter('wp_kses_allowed_html', function(array $allowed, string $context): array {
    if ($context === 'post') {
        $allowed['iframe'] = [
            'src'             => true,
            'width'           => true,
            'height'          => true,
            'frameborder'     => true,
            'allowfullscreen' => true,
        ];
    }
    return $allowed;
}, 10, 2);

// Modify authentication
add_filter('authenticate', function(?WP_User $user, string $username, string $password): WP_User|WP_Error|null {
    // Block login for specific conditions
    if ($username === 'admin') {
        return new WP_Error('invalid_username', __('Direct admin login is disabled.', 'my-plugin'));
    }
    return $user;
}, 30, 3);

// === REST API FILTERS ===

// Modify REST response
add_filter('rest_prepare_post', function(WP_REST_Response $response, WP_Post $post, WP_REST_Request $request): WP_REST_Response {
    // Add custom field to response
    $response->data['reading_time'] = my_plugin_calculate_reading_time($post->post_content);
    return $response;
}, 10, 3);
```

### Removing Filters

```php
<?php
/**
 * Remove filters
 */

// Remove wpautop (auto paragraphs)
remove_filter('the_content', 'wpautop');
remove_filter('the_excerpt', 'wpautop');

// Remove wptexturize (smart quotes)
remove_filter('the_content', 'wptexturize');
remove_filter('the_title', 'wptexturize');
remove_filter('comment_text', 'wptexturize');

// Remove specific filter (must match priority)
remove_filter('the_content', 'some_callback', 10);

// Remove all filters from a hook
remove_all_filters('the_content');

// Check if filter is applied
if (has_filter('the_content', 'some_callback')) {
    // Filter is registered
}
```

---

## Creating Custom Hooks

Allow other developers to extend your plugin/theme.

### Custom Actions

```php
<?php
declare(strict_types=1);

namespace MyPlugin;

/**
 * Example: Custom hooks in a plugin
 */
class OrderProcessor {

    /**
     * Process an order with custom hooks
     */
    public function process_order(array $order_data): int {
        // Allow modification of order data before processing
        $order_data = apply_filters('my_plugin_pre_process_order', $order_data);

        // Action before order creation
        do_action('my_plugin_before_create_order', $order_data);

        // Create the order
        $order_id = $this->create_order($order_data);

        if ($order_id) {
            // Action after successful order creation
            do_action('my_plugin_order_created', $order_id, $order_data);

            // Process payment
            $payment_result = $this->process_payment($order_id);

            if ($payment_result) {
                // Action after successful payment
                do_action('my_plugin_payment_complete', $order_id, $payment_result);
            } else {
                // Action on payment failure
                do_action('my_plugin_payment_failed', $order_id);
            }
        }

        // Action after all processing complete
        do_action('my_plugin_after_process_order', $order_id, $order_data);

        return $order_id;
    }

    /**
     * Get order total with filter
     */
    public function get_order_total(int $order_id): float {
        $subtotal = $this->calculate_subtotal($order_id);
        $shipping = $this->calculate_shipping($order_id);
        $tax = $this->calculate_tax($order_id);

        $total = $subtotal + $shipping + $tax;

        // Allow modification of total (for discounts, fees, etc.)
        return (float) apply_filters('my_plugin_order_total', $total, $order_id, [
            'subtotal' => $subtotal,
            'shipping' => $shipping,
            'tax'      => $tax,
        ]);
    }

    /**
     * Generate email content with filter
     */
    public function get_order_email_content(int $order_id): string {
        $order = $this->get_order($order_id);

        $content = sprintf(
            __('Order #%d has been placed.', 'my-plugin'),
            $order_id
        );

        // Allow complete override or modification
        return apply_filters('my_plugin_order_email_content', $content, $order_id, $order);
    }
}

/**
 * Example usage by another developer
 */

// Add discount to order total
add_filter('my_plugin_order_total', function(float $total, int $order_id, array $components): float {
    // Apply 10% discount for orders over $100
    if ($total > 100) {
        $total *= 0.9;
    }
    return $total;
}, 10, 3);

// Send notification on order creation
add_action('my_plugin_order_created', function(int $order_id, array $order_data): void {
    // Send Slack notification
    my_send_slack_notification("New order #{$order_id} created!");
}, 10, 2);

// Custom email content
add_filter('my_plugin_order_email_content', function(string $content, int $order_id, object $order): string {
    // Add custom footer
    $content .= "\n\nThank you for your business!";
    return $content;
}, 10, 3);
```

### Custom Filter with Default Value

```php
<?php
/**
 * Create filter with sensible defaults
 */

/**
 * Get items per page with filter
 */
function my_plugin_get_items_per_page(): int {
    $default = 10;

    /**
     * Filter the number of items per page
     *
     * @since 1.0.0
     *
     * @param int $items_per_page Number of items. Default 10.
     */
    return (int) apply_filters('my_plugin_items_per_page', $default);
}

/**
 * Get allowed file types with filter
 */
function my_plugin_get_allowed_file_types(): array {
    $defaults = ['jpg', 'jpeg', 'png', 'gif', 'pdf'];

    /**
     * Filter allowed file types for upload
     *
     * @since 1.0.0
     *
     * @param array $types Array of allowed file extensions.
     */
    return (array) apply_filters('my_plugin_allowed_file_types', $defaults);
}

/**
 * Check if feature is enabled with filter
 */
function my_plugin_is_feature_enabled(string $feature): bool {
    $enabled_features = [
        'dark_mode'    => true,
        'analytics'    => true,
        'beta_feature' => false,
    ];

    $is_enabled = $enabled_features[$feature] ?? false;

    /**
     * Filter whether a feature is enabled
     *
     * @since 1.0.0
     *
     * @param bool   $is_enabled Whether the feature is enabled.
     * @param string $feature    The feature slug.
     */
    return (bool) apply_filters('my_plugin_feature_enabled', $is_enabled, $feature);
}
```

---

## Hook Priority & Order

```php
<?php
/**
 * Priority determines execution order
 * Lower number = runs earlier
 * Default priority: 10
 */

// Runs first (priority 1)
add_action('init', 'my_first_function', 1);

// Runs with default priority (10)
add_action('init', 'my_default_function');
add_action('init', 'my_default_function_2'); // Runs after, same priority

// Runs last (priority 999)
add_action('init', 'my_last_function', 999);

/**
 * Filter priority example: Modify content
 */

// First: Add wrapper
add_filter('the_content', function(string $content): string {
    return '<div class="content-wrapper">' . $content . '</div>';
}, 5);

// Default: Add sharing buttons
add_filter('the_content', function(string $content): string {
    return $content . '<div class="share-buttons">...</div>';
}, 10);

// Late: Final output processing
add_filter('the_content', function(string $content): string {
    // Do final cleanup
    return $content;
}, 99);
```

---

## Best Practices

### Do

- Document custom hooks with PHPDoc comments
- Use prefixed hook names (`my_plugin_*`)
- Provide sensible default values for filters
- Pass relevant context to hooks (post ID, data arrays)
- Check `has_filter()`/`has_action()` before calling expensive operations
- Use appropriate priorities (don't default to 10 when order matters)
- Type hint callback parameters and return values (PHP 8.1+)
- Use namespaced functions or class methods as callbacks

### Do Not

- Remove core WordPress hooks without understanding consequences
- Create hooks that pass sensitive data (passwords, tokens)
- Rely on global variables in callbacks
- Forget to return filtered values
- Use anonymous functions when removal might be needed
- Create circular hook dependencies
- Add too many hooks at low priorities (performance impact)
- Modify data passed by reference unexpectedly

### Security Considerations

```php
<?php
/**
 * Security in hooks
 */

// Always validate/sanitize data from hooks
add_filter('my_plugin_user_input', function(mixed $input): string {
    return sanitize_text_field((string) $input);
});

// Check capabilities in action callbacks
add_action('my_plugin_admin_action', function(): void {
    if (!current_user_can('manage_options')) {
        wp_die(__('Unauthorized', 'my-plugin'));
    }
    // Proceed with admin action
});

// Verify nonces for form submissions
add_action('admin_post_my_plugin_save', function(): void {
    if (!wp_verify_nonce($_POST['_wpnonce'] ?? '', 'my_plugin_save')) {
        wp_die(__('Security check failed', 'my-plugin'));
    }
    // Process form
});
```

---

## Reference: Performance Security

# Performance & Security

---

## Performance Optimization

### Database Query Optimization

```php
<?php
declare(strict_types=1);

/**
 * Efficient database queries
 */

// BAD: Query inside loop
foreach ($post_ids as $post_id) {
    $meta = get_post_meta($post_id, 'my_key', true); // N+1 queries!
}

// GOOD: Batch query with caching
function get_posts_with_meta(array $post_ids): array {
    global $wpdb;

    $ids = implode(',', array_map('intval', $post_ids));

    // Single query for all meta
    $results = $wpdb->get_results($wpdb->prepare("
        SELECT post_id, meta_value
        FROM {$wpdb->postmeta}
        WHERE post_id IN ({$ids})
        AND meta_key = %s
    ", 'my_key'));

    $meta_map = [];
    foreach ($results as $row) {
        $meta_map[$row->post_id] = $row->meta_value;
    }

    return $meta_map;
}

/**
 * Use proper $wpdb methods with prepared statements
 */
function get_custom_data(int $user_id, string $status): array {
    global $wpdb;

    $table = $wpdb->prefix . 'custom_table';

    // GOOD: Prepared statement prevents SQL injection
    return $wpdb->get_results($wpdb->prepare("
        SELECT id, title, created_at
        FROM {$table}
        WHERE user_id = %d
        AND status = %s
        ORDER BY created_at DESC
        LIMIT 100
    ", $user_id, $status));
}

/**
 * Optimize WP_Query
 */
$optimized_query = new WP_Query([
    'post_type'              => 'product',
    'posts_per_page'         => 10,
    'no_found_rows'          => true,  // Skip SQL_CALC_FOUND_ROWS for pagination
    'update_post_meta_cache' => false, // Skip meta cache if not needed
    'update_post_term_cache' => false, // Skip term cache if not needed
    'fields'                 => 'ids', // Only get IDs if that's all you need
]);

/**
 * Use transients for expensive queries
 */
function get_popular_posts(): array {
    $cache_key = 'popular_posts_week';
    $posts = get_transient($cache_key);

    if ($posts === false) {
        $posts = get_posts([
            'post_type'      => 'post',
            'posts_per_page' => 10,
            'meta_key'       => 'views_count',
            'orderby'        => 'meta_value_num',
            'order'          => 'DESC',
            'date_query'     => [
                ['after' => '1 week ago'],
            ],
        ]);

        set_transient($cache_key, $posts, HOUR_IN_SECONDS);
    }

    return $posts;
}

/**
 * Invalidate cache when data changes
 */
add_action('save_post', function(int $post_id): void {
    delete_transient('popular_posts_week');
    delete_transient('featured_posts');
});
```

### Object Caching

```php
<?php
/**
 * WordPress object cache (works with Redis, Memcached)
 */

// Set cache
wp_cache_set('my_data', $data, 'my_plugin', 3600);

// Get cache
$data = wp_cache_get('my_data', 'my_plugin');
if ($data === false) {
    // Cache miss - fetch and set
    $data = expensive_operation();
    wp_cache_set('my_data', $data, 'my_plugin', 3600);
}

// Delete cache
wp_cache_delete('my_data', 'my_plugin');

// Cache with automatic handling
function get_expensive_data(int $id): mixed {
    $cache_key = 'expensive_data_' . $id;
    $cache_group = 'my_plugin';

    $data = wp_cache_get($cache_key, $cache_group);

    if ($data === false) {
        $data = perform_expensive_operation($id);
        wp_cache_set($cache_key, $data, $cache_group, HOUR_IN_SECONDS);
    }

    return $data;
}

/**
 * Fragment caching for expensive HTML
 */
function render_sidebar_widget(): void {
    $cache_key = 'sidebar_widget_html';
    $html = get_transient($cache_key);

    if ($html === false) {
        ob_start();
        // Expensive rendering
        include plugin_dir_path(__FILE__) . 'templates/widget.php';
        $html = ob_get_clean();

        set_transient($cache_key, $html, 15 * MINUTE_IN_SECONDS);
    }

    echo $html; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
}
```

### Asset Optimization

```php
<?php
/**
 * Efficient script and style loading
 */

// Conditional loading
add_action('wp_enqueue_scripts', function(): void {
    // Only load on specific pages
    if (!is_page('contact')) {
        return;
    }

    wp_enqueue_script('contact-form', ...);
});

// Defer non-critical scripts
add_filter('script_loader_tag', function(string $tag, string $handle): string {
    $defer_scripts = ['analytics', 'social-share', 'comments'];

    if (in_array($handle, $defer_scripts, true)) {
        return str_replace(' src', ' defer src', $tag);
    }

    return $tag;
}, 10, 2);

// Async scripts
add_filter('script_loader_tag', function(string $tag, string $handle): string {
    if ($handle === 'my-async-script') {
        return str_replace(' src', ' async src', $tag);
    }
    return $tag;
}, 10, 2);

// Preload critical assets
add_action('wp_head', function(): void {
    $font_url = get_template_directory_uri() . '/assets/fonts/inter.woff2';
    echo '<link rel="preload" href="' . esc_url($font_url) . '" as="font" type="font/woff2" crossorigin>';
}, 1);

// Remove unused scripts/styles
add_action('wp_enqueue_scripts', function(): void {
    // Remove block library CSS if not using blocks
    if (!is_singular()) {
        wp_dequeue_style('wp-block-library');
        wp_dequeue_style('wp-block-library-theme');
        wp_dequeue_style('global-styles');
    }

    // Remove emoji scripts
    remove_action('wp_head', 'print_emoji_detection_script', 7);
    remove_action('wp_print_styles', 'print_emoji_styles');
}, 100);

/**
 * Combine/minify inline styles
 */
add_action('wp_footer', function(): void {
    // Add critical CSS inline
    $critical_css = file_get_contents(get_template_directory() . '/assets/css/critical.css');
    if ($critical_css) {
        echo '<style id="critical-css">' . $critical_css . '</style>'; // phpcs:ignore
    }
}, 1);
```

### Image Optimization

```php
<?php
/**
 * Image optimization techniques
 */

// Add custom image sizes
add_action('after_setup_theme', function(): void {
    add_image_size('card-thumbnail', 400, 300, true);
    add_image_size('hero-image', 1600, 900, true);
});

// Lazy load images
add_filter('wp_get_attachment_image_attributes', function(array $attr): array {
    $attr['loading'] = 'lazy';
    $attr['decoding'] = 'async';
    return $attr;
});

// Add srcset for responsive images
add_filter('wp_calculate_image_srcset_meta', function(array $image_meta): array {
    // Ensure srcset is calculated
    return $image_meta;
});

// WebP support (requires server-side conversion)
add_filter('wp_generate_attachment_metadata', function(array $metadata, int $attachment_id): array {
    $file = get_attached_file($attachment_id);
    $mime = mime_content_type($file);

    if (in_array($mime, ['image/jpeg', 'image/png'], true)) {
        // Convert to WebP (requires Imagick or GD)
        my_plugin_create_webp_version($file);
    }

    return $metadata;
}, 10, 2);

// Serve WebP with fallback
function get_webp_image_url(string $url): string {
    $webp_url = preg_replace('/\.(jpe?g|png)$/i', '.webp', $url);
    $webp_path = str_replace(
        wp_upload_dir()['baseurl'],
        wp_upload_dir()['basedir'],
        $webp_url
    );

    if (file_exists($webp_path)) {
        return $webp_url;
    }

    return $url;
}
```

### Database Cleanup

```php
<?php
/**
 * Database maintenance
 */

// Clean up revisions (run via WP-CLI or cron)
function cleanup_post_revisions(int $keep = 5): int {
    global $wpdb;

    $deleted = 0;

    $posts = $wpdb->get_col("
        SELECT ID FROM {$wpdb->posts}
        WHERE post_type = 'revision'
        AND post_parent IN (
            SELECT ID FROM {$wpdb->posts} WHERE post_type IN ('post', 'page')
        )
    ");

    // Group by parent
    $by_parent = [];
    foreach ($posts as $revision_id) {
        $parent = wp_get_post_parent_id($revision_id);
        $by_parent[$parent][] = $revision_id;
    }

    foreach ($by_parent as $parent_id => $revisions) {
        // Keep most recent $keep revisions
        $to_delete = array_slice($revisions, $keep);
        foreach ($to_delete as $revision_id) {
            wp_delete_post_revision($revision_id);
            $deleted++;
        }
    }

    return $deleted;
}

// Clean up orphaned meta
function cleanup_orphaned_postmeta(): int {
    global $wpdb;

    return $wpdb->query("
        DELETE pm FROM {$wpdb->postmeta} pm
        LEFT JOIN {$wpdb->posts} p ON pm.post_id = p.ID
        WHERE p.ID IS NULL
    ");
}

// Clean up transients
function cleanup_expired_transients(): int {
    global $wpdb;

    $time = time();

    return $wpdb->query($wpdb->prepare("
        DELETE a, b FROM {$wpdb->options} a
        INNER JOIN {$wpdb->options} b ON b.option_name = CONCAT('_transient_timeout_', SUBSTRING(a.option_name, 12))
        WHERE a.option_name LIKE %s
        AND b.option_value < %d
    ", '_transient_%', $time));
}

// Schedule cleanup
add_action('init', function(): void {
    if (!wp_next_scheduled('my_plugin_db_cleanup')) {
        wp_schedule_event(time(), 'weekly', 'my_plugin_db_cleanup');
    }
});

add_action('my_plugin_db_cleanup', function(): void {
    cleanup_post_revisions(3);
    cleanup_orphaned_postmeta();
    cleanup_expired_transients();
});
```

---

## Security Hardening

### Input Sanitization

```php
<?php
declare(strict_types=1);

/**
 * Always sanitize user input
 */

// Text fields
$title = sanitize_text_field($_POST['title'] ?? '');
$email = sanitize_email($_POST['email'] ?? '');
$url = esc_url_raw($_POST['url'] ?? '');

// Textarea (allows line breaks)
$content = sanitize_textarea_field($_POST['content'] ?? '');

// HTML content (with allowed tags)
$html = wp_kses_post($_POST['html_content'] ?? '');

// Custom allowed HTML
$allowed_html = [
    'a'      => ['href' => [], 'title' => [], 'target' => []],
    'strong' => [],
    'em'     => [],
    'p'      => ['class' => []],
];
$safe_html = wp_kses($_POST['custom_html'] ?? '', $allowed_html);

// File names
$filename = sanitize_file_name($_POST['filename'] ?? '');

// Keys (alphanumeric, dashes, underscores)
$key = sanitize_key($_POST['key'] ?? '');

// Arrays
$ids = array_map('absint', (array) ($_POST['ids'] ?? []));
$tags = array_map('sanitize_text_field', (array) ($_POST['tags'] ?? []));

// Numbers
$id = absint($_POST['id'] ?? 0);
$price = (float) filter_var($_POST['price'] ?? 0, FILTER_SANITIZE_NUMBER_FLOAT, FILTER_FLAG_ALLOW_FRACTION);

/**
 * Database-safe queries
 */
global $wpdb;

// ALWAYS use prepared statements
$results = $wpdb->get_results($wpdb->prepare("
    SELECT * FROM {$wpdb->prefix}custom_table
    WHERE user_id = %d
    AND status = %s
    AND created_at > %s
", $user_id, $status, $date));

// Insert with proper escaping
$wpdb->insert(
    $wpdb->prefix . 'custom_table',
    [
        'user_id' => $user_id,
        'title'   => $title,
        'content' => $content,
    ],
    ['%d', '%s', '%s']
);

// Update with proper escaping
$wpdb->update(
    $wpdb->prefix . 'custom_table',
    ['title' => $new_title],
    ['id' => $id],
    ['%s'],
    ['%d']
);
```

### Output Escaping

```php
<?php
/**
 * Always escape output
 */

// HTML context
echo '<h1>' . esc_html($title) . '</h1>';
echo '<p>' . esc_html__('Welcome', 'my-plugin') . '</p>';

// Attributes
echo '<input type="text" value="' . esc_attr($value) . '" />';
echo '<div class="' . esc_attr($class) . '">';
echo '<div data-config="' . esc_attr(wp_json_encode($config)) . '">';

// URLs
echo '<a href="' . esc_url($url) . '">' . esc_html($text) . '</a>';
echo '<img src="' . esc_url($image_url) . '" alt="' . esc_attr($alt) . '" />';

// JavaScript
echo '<script>var config = ' . wp_json_encode($config) . ';</script>';

// Textarea content
echo '<textarea>' . esc_textarea($content) . '</textarea>';

// Allow specific HTML
echo wp_kses_post($html_content);

// Translation with escaping
printf(
    /* translators: %s: user name */
    esc_html__('Hello, %s!', 'my-plugin'),
    esc_html($user_name)
);

/**
 * When outputting large blocks of HTML
 */
?>
<div class="card">
    <h2><?php echo esc_html($card_title); ?></h2>
    <p><?php echo wp_kses_post($card_content); ?></p>
    <a href="<?php echo esc_url($card_link); ?>" class="<?php echo esc_attr($card_class); ?>">
        <?php echo esc_html($card_cta); ?>
    </a>
</div>
<?php
```

### Nonce Verification

```php
<?php
/**
 * Nonces prevent CSRF attacks
 */

// In form
function render_settings_form(): void {
    ?>
    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
        <?php wp_nonce_field('my_plugin_save_settings', 'my_plugin_nonce'); ?>
        <input type="hidden" name="action" value="my_plugin_save_settings" />

        <!-- Form fields -->

        <?php submit_button(__('Save Settings', 'my-plugin')); ?>
    </form>
    <?php
}

// Verify nonce on submission
add_action('admin_post_my_plugin_save_settings', function(): void {
    // Verify nonce
    if (!wp_verify_nonce($_POST['my_plugin_nonce'] ?? '', 'my_plugin_save_settings')) {
        wp_die(
            esc_html__('Security check failed.', 'my-plugin'),
            esc_html__('Error', 'my-plugin'),
            ['response' => 403]
        );
    }

    // Verify capability
    if (!current_user_can('manage_options')) {
        wp_die(
            esc_html__('You do not have permission to perform this action.', 'my-plugin'),
            esc_html__('Error', 'my-plugin'),
            ['response' => 403]
        );
    }

    // Process form
    $settings = [
        'option_1' => sanitize_text_field($_POST['option_1'] ?? ''),
        'option_2' => absint($_POST['option_2'] ?? 0),
    ];

    update_option('my_plugin_settings', $settings);

    wp_safe_redirect(add_query_arg('updated', 'true', wp_get_referer()));
    exit;
});

/**
 * AJAX with nonce
 */

// Localize script with nonce
wp_localize_script('my-script', 'myPluginData', [
    'ajaxUrl' => admin_url('admin-ajax.php'),
    'nonce'   => wp_create_nonce('my_plugin_ajax'),
]);

// JavaScript
// fetch(myPluginData.ajaxUrl, {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
//     body: new URLSearchParams({
//         action: 'my_plugin_action',
//         nonce: myPluginData.nonce,
//         data: 'value'
//     })
// });

// Handle AJAX
add_action('wp_ajax_my_plugin_action', function(): void {
    check_ajax_referer('my_plugin_ajax', 'nonce');

    if (!current_user_can('edit_posts')) {
        wp_send_json_error(['message' => 'Unauthorized'], 403);
    }

    $data = sanitize_text_field($_POST['data'] ?? '');

    // Process request
    $result = process_data($data);

    wp_send_json_success(['result' => $result]);
});
```

### Capability Checks

```php
<?php
/**
 * Always verify user capabilities
 */

// Check before displaying admin page
function render_admin_page(): void {
    if (!current_user_can('manage_options')) {
        wp_die(__('You do not have permission to access this page.', 'my-plugin'));
    }

    // Render page
}

// Check before performing action
function delete_item(int $item_id): bool {
    if (!current_user_can('delete_posts')) {
        return false;
    }

    // Delete item
    return true;
}

// Meta capability check for specific post
function edit_custom_post(int $post_id): bool {
    if (!current_user_can('edit_post', $post_id)) {
        return false;
    }

    // Edit post
    return true;
}

/**
 * Custom capabilities
 */

// Add custom capabilities on activation
function add_custom_capabilities(): void {
    $admin = get_role('administrator');
    $editor = get_role('editor');

    if ($admin) {
        $admin->add_cap('manage_my_plugin');
        $admin->add_cap('edit_my_plugin_items');
        $admin->add_cap('delete_my_plugin_items');
    }

    if ($editor) {
        $editor->add_cap('edit_my_plugin_items');
    }
}

// Use custom capability
if (current_user_can('manage_my_plugin')) {
    // Show management interface
}

// Map meta capabilities
add_filter('map_meta_cap', function(array $caps, string $cap, int $user_id, array $args): array {
    if ($cap === 'edit_my_plugin_item') {
        $item_id = $args[0] ?? 0;
        $item = get_my_plugin_item($item_id);

        if ($item && $item->author_id === $user_id) {
            $caps = ['edit_my_plugin_items'];
        } else {
            $caps = ['manage_my_plugin'];
        }
    }

    return $caps;
}, 10, 4);
```

### File Upload Security

```php
<?php
/**
 * Secure file upload handling
 */

function handle_file_upload(): array|WP_Error {
    // Verify nonce and capability
    if (!wp_verify_nonce($_POST['nonce'] ?? '', 'my_plugin_upload')) {
        return new WP_Error('security', __('Security check failed.', 'my-plugin'));
    }

    if (!current_user_can('upload_files')) {
        return new WP_Error('permission', __('You cannot upload files.', 'my-plugin'));
    }

    // Check file exists
    if (empty($_FILES['my_file']['tmp_name'])) {
        return new WP_Error('no_file', __('No file uploaded.', 'my-plugin'));
    }

    $file = $_FILES['my_file'];

    // Validate file type
    $allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'];
    $file_type = wp_check_filetype_and_ext($file['tmp_name'], $file['name']);

    if (!in_array($file_type['type'], $allowed_types, true)) {
        return new WP_Error('invalid_type', __('File type not allowed.', 'my-plugin'));
    }

    // Validate file size (5MB max)
    $max_size = 5 * 1024 * 1024;
    if ($file['size'] > $max_size) {
        return new WP_Error('too_large', __('File is too large.', 'my-plugin'));
    }

    // Sanitize filename
    $filename = sanitize_file_name($file['name']);

    // Use WordPress upload handling
    require_once ABSPATH . 'wp-admin/includes/file.php';
    require_once ABSPATH . 'wp-admin/includes/media.php';
    require_once ABSPATH . 'wp-admin/includes/image.php';

    // Handle upload
    $upload = wp_handle_upload($file, [
        'test_form' => false,
        'mimes'     => [
            'jpg|jpeg' => 'image/jpeg',
            'png'      => 'image/png',
            'gif'      => 'image/gif',
            'pdf'      => 'application/pdf',
        ],
    ]);

    if (isset($upload['error'])) {
        return new WP_Error('upload_error', $upload['error']);
    }

    // Create attachment
    $attachment_id = wp_insert_attachment([
        'post_mime_type' => $upload['type'],
        'post_title'     => preg_replace('/\.[^.]+$/', '', $filename),
        'post_content'   => '',
        'post_status'    => 'inherit',
    ], $upload['file']);

    // Generate metadata
    $metadata = wp_generate_attachment_metadata($attachment_id, $upload['file']);
    wp_update_attachment_metadata($attachment_id, $metadata);

    return [
        'id'  => $attachment_id,
        'url' => $upload['url'],
    ];
}
```

### Security Headers

```php
<?php
/**
 * Add security headers
 */

add_action('send_headers', function(): void {
    // Only on frontend, not admin or REST
    if (is_admin() || defined('REST_REQUEST')) {
        return;
    }

    // Prevent clickjacking
    header('X-Frame-Options: SAMEORIGIN');

    // Prevent MIME sniffing
    header('X-Content-Type-Options: nosniff');

    // XSS Protection
    header('X-XSS-Protection: 1; mode=block');

    // Referrer Policy
    header('Referrer-Policy: strict-origin-when-cross-origin');

    // Content Security Policy (customize as needed)
    $csp = "default-src 'self'; " .
           "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.google-analytics.com; " .
           "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; " .
           "font-src 'self' https://fonts.gstatic.com; " .
           "img-src 'self' data: https:; " .
           "connect-src 'self' https://www.google-analytics.com;";

    header("Content-Security-Policy: {$csp}");

    // Permissions Policy
    header("Permissions-Policy: geolocation=(), microphone=(), camera=()");
});
```

### Login Security

```php
<?php
/**
 * Login security enhancements
 */

// Limit login attempts
add_filter('authenticate', function(?WP_User $user, string $username, string $password): WP_User|WP_Error|null {
    if (empty($username) || empty($password)) {
        return $user;
    }

    $ip = $_SERVER['REMOTE_ADDR'];
    $lockout_key = 'login_attempts_' . md5($ip);
    $attempts = (int) get_transient($lockout_key);

    if ($attempts >= 5) {
        return new WP_Error(
            'too_many_attempts',
            sprintf(
                __('Too many failed login attempts. Please try again in %d minutes.', 'my-plugin'),
                15
            )
        );
    }

    return $user;
}, 20, 3);

// Track failed attempts
add_action('wp_login_failed', function(string $username): void {
    $ip = $_SERVER['REMOTE_ADDR'];
    $lockout_key = 'login_attempts_' . md5($ip);
    $attempts = (int) get_transient($lockout_key);

    set_transient($lockout_key, $attempts + 1, 15 * MINUTE_IN_SECONDS);
});

// Clear on successful login
add_action('wp_login', function(string $username): void {
    $ip = $_SERVER['REMOTE_ADDR'];
    $lockout_key = 'login_attempts_' . md5($ip);
    delete_transient($lockout_key);
});

// Disable XML-RPC if not needed
add_filter('xmlrpc_enabled', '__return_false');

// Hide login errors (don't reveal if username exists)
add_filter('login_errors', function(): string {
    return __('Invalid login credentials.', 'my-plugin');
});

// Force strong passwords
add_action('user_profile_update_errors', function(WP_Error $errors, bool $update, object $user): void {
    $password = $_POST['pass1'] ?? '';

    if (!empty($password)) {
        // Require minimum 12 characters
        if (strlen($password) < 12) {
            $errors->add('weak_password', __('Password must be at least 12 characters.', 'my-plugin'));
        }

        // Require mixed case, numbers, special chars
        if (!preg_match('/[A-Z]/', $password) ||
            !preg_match('/[a-z]/', $password) ||
            !preg_match('/[0-9]/', $password) ||
            !preg_match('/[^A-Za-z0-9]/', $password)) {
            $errors->add('weak_password', __('Password must contain uppercase, lowercase, numbers, and special characters.', 'my-plugin'));
        }
    }
}, 10, 3);
```

---

## Backup Strategy

```php
<?php
/**
 * Backup implementation
 */

class Database_Backup {

    private string $backup_dir;

    public function __construct() {
        $upload_dir = wp_upload_dir();
        $this->backup_dir = $upload_dir['basedir'] . '/backups/';

        if (!file_exists($this->backup_dir)) {
            wp_mkdir_p($this->backup_dir);

            // Protect directory
            file_put_contents($this->backup_dir . '.htaccess', 'deny from all');
            file_put_contents($this->backup_dir . 'index.php', '<?php // Silence is golden');
        }
    }

    /**
     * Create database backup
     */
    public function create_backup(): string|WP_Error {
        global $wpdb;

        $filename = 'db-backup-' . date('Y-m-d-His') . '.sql';
        $filepath = $this->backup_dir . $filename;

        $tables = $wpdb->get_col('SHOW TABLES');
        $output = "-- WordPress Database Backup\n";
        $output .= "-- Generated: " . date('Y-m-d H:i:s') . "\n\n";

        foreach ($tables as $table) {
            // Skip non-WordPress tables
            if (strpos($table, $wpdb->prefix) !== 0) {
                continue;
            }

            $output .= "DROP TABLE IF EXISTS `{$table}`;\n";

            $create = $wpdb->get_row("SHOW CREATE TABLE `{$table}`", ARRAY_N);
            $output .= $create[1] . ";\n\n";

            $rows = $wpdb->get_results("SELECT * FROM `{$table}`", ARRAY_A);

            foreach ($rows as $row) {
                $values = array_map(function($value) use ($wpdb) {
                    return $value === null ? 'NULL' : "'" . $wpdb->_real_escape($value) . "'";
                }, $row);

                $output .= "INSERT INTO `{$table}` VALUES (" . implode(',', $values) . ");\n";
            }

            $output .= "\n";
        }

        if (file_put_contents($filepath, $output) === false) {
            return new WP_Error('backup_failed', __('Failed to write backup file.', 'my-plugin'));
        }

        // Compress
        if (function_exists('gzencode')) {
            $compressed = gzencode($output, 9);
            file_put_contents($filepath . '.gz', $compressed);
            unlink($filepath);
            $filepath .= '.gz';
        }

        return $filepath;
    }

    /**
     * Clean old backups
     */
    public function cleanup_old_backups(int $keep_days = 30): int {
        $deleted = 0;
        $files = glob($this->backup_dir . '*.sql*');
        $cutoff = time() - ($keep_days * DAY_IN_SECONDS);

        foreach ($files as $file) {
            if (filemtime($file) < $cutoff) {
                unlink($file);
                $deleted++;
            }
        }

        return $deleted;
    }
}

// Schedule automatic backups
add_action('init', function(): void {
    if (!wp_next_scheduled('my_plugin_daily_backup')) {
        wp_schedule_event(time(), 'daily', 'my_plugin_daily_backup');
    }
});

add_action('my_plugin_daily_backup', function(): void {
    $backup = new Database_Backup();
    $result = $backup->create_backup();

    if (!is_wp_error($result)) {
        $backup->cleanup_old_backups(7);
    }
});
```

---

## Best Practices Summary

### Performance

- Use object caching (Redis/Memcached)
- Implement transients for expensive operations
- Optimize database queries with proper indexes
- Lazy load images and defer non-critical scripts
- Use `no_found_rows` when pagination not needed
- Clean up revisions and transients regularly

### Security

- Sanitize ALL user input
- Escape ALL output
- Use nonces for all form submissions and AJAX
- Verify capabilities before any action
- Use prepared statements for database queries
- Validate file uploads thoroughly
- Implement rate limiting for login
- Add security headers
- Keep WordPress and plugins updated

---

## Reference: Plugin Architecture

# Plugin Architecture

---

## Plugin Structure

### Minimal Plugin Structure

```
plugin-name/
├── plugin-name.php        # Main plugin file with header
├── uninstall.php          # Cleanup on uninstall
├── includes/
│   ├── class-plugin-name.php
│   ├── class-activator.php
│   ├── class-deactivator.php
│   └── class-loader.php
├── admin/
│   ├── class-admin.php
│   ├── css/
│   └── js/
├── public/
│   ├── class-public.php
│   ├── css/
│   └── js/
├── languages/
│   └── plugin-name.pot
└── README.txt
```

### Full Plugin Structure (Enterprise)

```
plugin-name/
├── plugin-name.php
├── uninstall.php
├── composer.json
├── phpcs.xml.dist
├── phpunit.xml.dist
├── includes/
│   ├── class-plugin.php           # Main plugin class
│   ├── class-activator.php        # Activation logic
│   ├── class-deactivator.php      # Deactivation logic
│   ├── class-loader.php           # Hook loader
│   ├── class-i18n.php             # Internationalization
│   ├── Traits/
│   │   └── Singleton.php
│   ├── Interfaces/
│   │   ├── Registrable.php
│   │   └── Hookable.php
│   ├── Services/
│   │   └── class-api-service.php
│   └── Repositories/
│       └── class-data-repository.php
├── admin/
│   ├── class-admin.php
│   ├── class-settings.php
│   ├── partials/
│   │   └── settings-page.php
│   ├── css/
│   └── js/
├── public/
│   ├── class-frontend.php
│   ├── partials/
│   ├── css/
│   └── js/
├── blocks/
│   └── custom-block/
├── templates/
│   └── single-custom-type.php
├── languages/
├── tests/
│   ├── bootstrap.php
│   └── unit/
└── vendor/
```

---

## Main Plugin File

### Plugin Header

```php
<?php
/**
 * Plugin Name:       Plugin Name
 * Plugin URI:        https://example.com/plugin-name
 * Description:       A brief description of what this plugin does.
 * Version:           1.0.0
 * Requires at least: 6.4
 * Requires PHP:      8.1
 * Author:            Author Name
 * Author URI:        https://example.com
 * License:           GPL v2 or later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       plugin-name
 * Domain Path:       /languages
 * Update URI:        https://example.com/plugin-name
 *
 * @package PluginName
 */

declare(strict_types=1);

namespace PluginName;

// Prevent direct access
defined('ABSPATH') || exit;

// Plugin constants
define('PLUGIN_NAME_VERSION', '1.0.0');
define('PLUGIN_NAME_FILE', __FILE__);
define('PLUGIN_NAME_PATH', plugin_dir_path(__FILE__));
define('PLUGIN_NAME_URL', plugin_dir_url(__FILE__));
define('PLUGIN_NAME_BASENAME', plugin_basename(__FILE__));

// Autoloader
if (file_exists(PLUGIN_NAME_PATH . 'vendor/autoload.php')) {
    require_once PLUGIN_NAME_PATH . 'vendor/autoload.php';
}

// Manual includes if no autoloader
require_once PLUGIN_NAME_PATH . 'includes/class-plugin.php';
require_once PLUGIN_NAME_PATH . 'includes/class-activator.php';
require_once PLUGIN_NAME_PATH . 'includes/class-deactivator.php';

/**
 * Plugin activation hook
 */
function activate(): void {
    Activator::activate();
}
register_activation_hook(__FILE__, __NAMESPACE__ . '\\activate');

/**
 * Plugin deactivation hook
 */
function deactivate(): void {
    Deactivator::deactivate();
}
register_deactivation_hook(__FILE__, __NAMESPACE__ . '\\deactivate');

/**
 * Initialize the plugin
 */
function init(): void {
    $plugin = new Plugin();
    $plugin->run();
}
add_action('plugins_loaded', __NAMESPACE__ . '\\init');
```

---

## Activation & Deactivation

### Activator Class

```php
<?php
declare(strict_types=1);

namespace PluginName;

/**
 * Fired during plugin activation
 */
class Activator {

    /**
     * Activation tasks
     */
    public static function activate(): void {
        // Check requirements
        self::check_requirements();

        // Create database tables
        self::create_tables();

        // Set default options
        self::set_default_options();

        // Schedule cron events
        self::schedule_events();

        // Add capabilities
        self::add_capabilities();

        // Flush rewrite rules (if registering CPT/taxonomy)
        flush_rewrite_rules();

        // Set activation flag for welcome notice
        set_transient('plugin_name_activated', true, 30);
    }

    /**
     * Check system requirements
     */
    private static function check_requirements(): void {
        if (version_compare(PHP_VERSION, '8.1', '<')) {
            deactivate_plugins(PLUGIN_NAME_BASENAME);
            wp_die(
                esc_html__('This plugin requires PHP 8.1 or higher.', 'plugin-name'),
                'Plugin Activation Error',
                ['back_link' => true]
            );
        }

        global $wp_version;
        if (version_compare($wp_version, '6.4', '<')) {
            deactivate_plugins(PLUGIN_NAME_BASENAME);
            wp_die(
                esc_html__('This plugin requires WordPress 6.4 or higher.', 'plugin-name'),
                'Plugin Activation Error',
                ['back_link' => true]
            );
        }
    }

    /**
     * Create custom database tables
     */
    private static function create_tables(): void {
        global $wpdb;

        $charset_collate = $wpdb->get_charset_collate();
        $table_name = $wpdb->prefix . 'plugin_name_data';

        $sql = "CREATE TABLE IF NOT EXISTS {$table_name} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            user_id bigint(20) unsigned NOT NULL DEFAULT 0,
            data_key varchar(191) NOT NULL,
            data_value longtext,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY user_id (user_id),
            KEY data_key (data_key)
        ) {$charset_collate};";

        require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        dbDelta($sql);

        // Store DB version
        update_option('plugin_name_db_version', PLUGIN_NAME_VERSION);
    }

    /**
     * Set default options
     */
    private static function set_default_options(): void {
        $defaults = [
            'enabled'          => true,
            'api_key'          => '',
            'cache_duration'   => 3600,
            'items_per_page'   => 10,
            'allowed_roles'    => ['administrator', 'editor'],
        ];

        if (get_option('plugin_name_settings') === false) {
            add_option('plugin_name_settings', $defaults);
        }
    }

    /**
     * Schedule cron events
     */
    private static function schedule_events(): void {
        if (!wp_next_scheduled('plugin_name_daily_cleanup')) {
            wp_schedule_event(time(), 'daily', 'plugin_name_daily_cleanup');
        }
    }

    /**
     * Add custom capabilities
     */
    private static function add_capabilities(): void {
        $admin = get_role('administrator');
        if ($admin) {
            $admin->add_cap('manage_plugin_name');
            $admin->add_cap('edit_plugin_name_data');
        }
    }
}
```

### Deactivator Class

```php
<?php
declare(strict_types=1);

namespace PluginName;

/**
 * Fired during plugin deactivation
 */
class Deactivator {

    /**
     * Deactivation tasks
     */
    public static function deactivate(): void {
        // Clear scheduled events
        self::clear_scheduled_events();

        // Clear transients
        self::clear_transients();

        // Flush rewrite rules
        flush_rewrite_rules();

        // Note: Do NOT delete options or tables here
        // That should only happen in uninstall.php
    }

    /**
     * Clear all scheduled cron events
     */
    private static function clear_scheduled_events(): void {
        $timestamp = wp_next_scheduled('plugin_name_daily_cleanup');
        if ($timestamp) {
            wp_unschedule_event($timestamp, 'plugin_name_daily_cleanup');
        }

        // Clear all instances of our events
        wp_clear_scheduled_hook('plugin_name_daily_cleanup');
    }

    /**
     * Clear transients
     */
    private static function clear_transients(): void {
        global $wpdb;

        // Clear specific transients
        delete_transient('plugin_name_cache');
        delete_transient('plugin_name_activated');

        // Clear all plugin transients (use with caution)
        $wpdb->query(
            $wpdb->prepare(
                "DELETE FROM {$wpdb->options} WHERE option_name LIKE %s OR option_name LIKE %s",
                '_transient_plugin_name_%',
                '_transient_timeout_plugin_name_%'
            )
        );
    }
}
```

### uninstall.php

```php
<?php
/**
 * Uninstall script - runs when plugin is deleted
 *
 * @package PluginName
 */

// If uninstall not called from WordPress, exit
if (!defined('WP_UNINSTALL_PLUGIN')) {
    exit;
}

// Check if we should preserve data
$settings = get_option('plugin_name_settings', []);
$preserve_data = $settings['preserve_data_on_uninstall'] ?? false;

if (!$preserve_data) {
    global $wpdb;

    // Delete options
    delete_option('plugin_name_settings');
    delete_option('plugin_name_db_version');

    // Delete user meta
    $wpdb->query("DELETE FROM {$wpdb->usermeta} WHERE meta_key LIKE 'plugin_name_%'");

    // Delete post meta
    $wpdb->query("DELETE FROM {$wpdb->postmeta} WHERE meta_key LIKE '_plugin_name_%'");

    // Delete custom tables
    $wpdb->query("DROP TABLE IF EXISTS {$wpdb->prefix}plugin_name_data");

    // Delete transients
    $wpdb->query(
        $wpdb->prepare(
            "DELETE FROM {$wpdb->options} WHERE option_name LIKE %s OR option_name LIKE %s",
            '_transient_plugin_name_%',
            '_transient_timeout_plugin_name_%'
        )
    );

    // Remove capabilities
    $roles = ['administrator', 'editor'];
    foreach ($roles as $role_name) {
        $role = get_role($role_name);
        if ($role) {
            $role->remove_cap('manage_plugin_name');
            $role->remove_cap('edit_plugin_name_data');
        }
    }

    // Clear any cached data
    wp_cache_flush();
}
```

---

## Settings API

### Settings Class

```php
<?php
declare(strict_types=1);

namespace PluginName\Admin;

/**
 * Plugin settings management
 */
class Settings {

    private const OPTION_GROUP = 'plugin_name_settings';
    private const OPTION_NAME = 'plugin_name_settings';
    private const PAGE_SLUG = 'plugin-name-settings';

    /**
     * Initialize settings
     */
    public function init(): void {
        add_action('admin_menu', [$this, 'add_menu_page']);
        add_action('admin_init', [$this, 'register_settings']);
    }

    /**
     * Add admin menu page
     */
    public function add_menu_page(): void {
        add_options_page(
            __('Plugin Name Settings', 'plugin-name'),
            __('Plugin Name', 'plugin-name'),
            'manage_options',
            self::PAGE_SLUG,
            [$this, 'render_settings_page']
        );
    }

    /**
     * Register all settings
     */
    public function register_settings(): void {
        register_setting(
            self::OPTION_GROUP,
            self::OPTION_NAME,
            [
                'type'              => 'array',
                'sanitize_callback' => [$this, 'sanitize_settings'],
                'default'           => $this->get_defaults(),
            ]
        );

        // General section
        add_settings_section(
            'plugin_name_general',
            __('General Settings', 'plugin-name'),
            [$this, 'render_general_section'],
            self::PAGE_SLUG
        );

        // API section
        add_settings_section(
            'plugin_name_api',
            __('API Settings', 'plugin-name'),
            [$this, 'render_api_section'],
            self::PAGE_SLUG
        );

        // Fields
        $this->add_fields();
    }

    /**
     * Add settings fields
     */
    private function add_fields(): void {
        // Enable field
        add_settings_field(
            'enabled',
            __('Enable Plugin', 'plugin-name'),
            [$this, 'render_checkbox_field'],
            self::PAGE_SLUG,
            'plugin_name_general',
            [
                'label_for'   => 'enabled',
                'description' => __('Enable or disable the plugin functionality.', 'plugin-name'),
            ]
        );

        // Items per page
        add_settings_field(
            'items_per_page',
            __('Items Per Page', 'plugin-name'),
            [$this, 'render_number_field'],
            self::PAGE_SLUG,
            'plugin_name_general',
            [
                'label_for'   => 'items_per_page',
                'min'         => 1,
                'max'         => 100,
                'description' => __('Number of items to display per page.', 'plugin-name'),
            ]
        );

        // API Key
        add_settings_field(
            'api_key',
            __('API Key', 'plugin-name'),
            [$this, 'render_text_field'],
            self::PAGE_SLUG,
            'plugin_name_api',
            [
                'label_for'   => 'api_key',
                'type'        => 'password',
                'description' => __('Enter your API key for external service.', 'plugin-name'),
            ]
        );

        // Cache duration
        add_settings_field(
            'cache_duration',
            __('Cache Duration', 'plugin-name'),
            [$this, 'render_select_field'],
            self::PAGE_SLUG,
            'plugin_name_api',
            [
                'label_for'   => 'cache_duration',
                'options'     => [
                    '900'   => __('15 minutes', 'plugin-name'),
                    '1800'  => __('30 minutes', 'plugin-name'),
                    '3600'  => __('1 hour', 'plugin-name'),
                    '86400' => __('1 day', 'plugin-name'),
                ],
                'description' => __('How long to cache API responses.', 'plugin-name'),
            ]
        );
    }

    /**
     * Get default settings
     */
    private function get_defaults(): array {
        return [
            'enabled'        => true,
            'api_key'        => '',
            'cache_duration' => 3600,
            'items_per_page' => 10,
        ];
    }

    /**
     * Sanitize settings
     */
    public function sanitize_settings(array $input): array {
        $sanitized = [];

        $sanitized['enabled'] = !empty($input['enabled']);

        $sanitized['api_key'] = sanitize_text_field($input['api_key'] ?? '');

        $sanitized['cache_duration'] = absint($input['cache_duration'] ?? 3600);
        if (!in_array($sanitized['cache_duration'], [900, 1800, 3600, 86400], true)) {
            $sanitized['cache_duration'] = 3600;
        }

        $sanitized['items_per_page'] = absint($input['items_per_page'] ?? 10);
        $sanitized['items_per_page'] = max(1, min(100, $sanitized['items_per_page']));

        return $sanitized;
    }

    /**
     * Render settings page
     */
    public function render_settings_page(): void {
        if (!current_user_can('manage_options')) {
            return;
        }

        // Show success message
        if (isset($_GET['settings-updated'])) {
            add_settings_error(
                self::OPTION_GROUP,
                'settings_updated',
                __('Settings saved.', 'plugin-name'),
                'updated'
            );
        }
        ?>
        <div class="wrap">
            <h1><?php echo esc_html(get_admin_page_title()); ?></h1>

            <?php settings_errors(self::OPTION_GROUP); ?>

            <form action="options.php" method="post">
                <?php
                settings_fields(self::OPTION_GROUP);
                do_settings_sections(self::PAGE_SLUG);
                submit_button(__('Save Settings', 'plugin-name'));
                ?>
            </form>
        </div>
        <?php
    }

    /**
     * Render general section description
     */
    public function render_general_section(): void {
        echo '<p>' . esc_html__('Configure general plugin settings.', 'plugin-name') . '</p>';
    }

    /**
     * Render API section description
     */
    public function render_api_section(): void {
        echo '<p>' . esc_html__('Configure API connection settings.', 'plugin-name') . '</p>';
    }

    /**
     * Render checkbox field
     */
    public function render_checkbox_field(array $args): void {
        $options = get_option(self::OPTION_NAME, $this->get_defaults());
        $value = $options[$args['label_for']] ?? false;
        ?>
        <input type="checkbox"
               id="<?php echo esc_attr($args['label_for']); ?>"
               name="<?php echo esc_attr(self::OPTION_NAME . '[' . $args['label_for'] . ']'); ?>"
               value="1"
               <?php checked($value, true); ?>
        />
        <?php if (!empty($args['description'])): ?>
            <p class="description"><?php echo esc_html($args['description']); ?></p>
        <?php endif;
    }

    /**
     * Render text field
     */
    public function render_text_field(array $args): void {
        $options = get_option(self::OPTION_NAME, $this->get_defaults());
        $value = $options[$args['label_for']] ?? '';
        $type = $args['type'] ?? 'text';
        ?>
        <input type="<?php echo esc_attr($type); ?>"
               id="<?php echo esc_attr($args['label_for']); ?>"
               name="<?php echo esc_attr(self::OPTION_NAME . '[' . $args['label_for'] . ']'); ?>"
               value="<?php echo esc_attr($value); ?>"
               class="regular-text"
        />
        <?php if (!empty($args['description'])): ?>
            <p class="description"><?php echo esc_html($args['description']); ?></p>
        <?php endif;
    }

    /**
     * Render number field
     */
    public function render_number_field(array $args): void {
        $options = get_option(self::OPTION_NAME, $this->get_defaults());
        $value = $options[$args['label_for']] ?? 0;
        ?>
        <input type="number"
               id="<?php echo esc_attr($args['label_for']); ?>"
               name="<?php echo esc_attr(self::OPTION_NAME . '[' . $args['label_for'] . ']'); ?>"
               value="<?php echo esc_attr($value); ?>"
               min="<?php echo esc_attr($args['min'] ?? 0); ?>"
               max="<?php echo esc_attr($args['max'] ?? 100); ?>"
               class="small-text"
        />
        <?php if (!empty($args['description'])): ?>
            <p class="description"><?php echo esc_html($args['description']); ?></p>
        <?php endif;
    }

    /**
     * Render select field
     */
    public function render_select_field(array $args): void {
        $options = get_option(self::OPTION_NAME, $this->get_defaults());
        $value = $options[$args['label_for']] ?? '';
        ?>
        <select id="<?php echo esc_attr($args['label_for']); ?>"
                name="<?php echo esc_attr(self::OPTION_NAME . '[' . $args['label_for'] . ']'); ?>">
            <?php foreach ($args['options'] as $key => $label): ?>
                <option value="<?php echo esc_attr($key); ?>" <?php selected($value, $key); ?>>
                    <?php echo esc_html($label); ?>
                </option>
            <?php endforeach; ?>
        </select>
        <?php if (!empty($args['description'])): ?>
            <p class="description"><?php echo esc_html($args['description']); ?></p>
        <?php endif;
    }
}
```

---

## Custom Post Types & Taxonomies

### Registering Custom Post Types

```php
<?php
declare(strict_types=1);

namespace PluginName;

/**
 * Register custom post types and taxonomies
 */
class CustomPostTypes {

    /**
     * Initialize
     */
    public function init(): void {
        add_action('init', [$this, 'register_post_types']);
        add_action('init', [$this, 'register_taxonomies']);
    }

    /**
     * Register custom post type
     */
    public function register_post_types(): void {
        $labels = [
            'name'                  => _x('Products', 'Post Type General Name', 'plugin-name'),
            'singular_name'         => _x('Product', 'Post Type Singular Name', 'plugin-name'),
            'menu_name'             => __('Products', 'plugin-name'),
            'name_admin_bar'        => __('Product', 'plugin-name'),
            'archives'              => __('Product Archives', 'plugin-name'),
            'attributes'            => __('Product Attributes', 'plugin-name'),
            'parent_item_colon'     => __('Parent Product:', 'plugin-name'),
            'all_items'             => __('All Products', 'plugin-name'),
            'add_new_item'          => __('Add New Product', 'plugin-name'),
            'add_new'               => __('Add New', 'plugin-name'),
            'new_item'              => __('New Product', 'plugin-name'),
            'edit_item'             => __('Edit Product', 'plugin-name'),
            'update_item'           => __('Update Product', 'plugin-name'),
            'view_item'             => __('View Product', 'plugin-name'),
            'view_items'            => __('View Products', 'plugin-name'),
            'search_items'          => __('Search Product', 'plugin-name'),
            'not_found'             => __('Not found', 'plugin-name'),
            'not_found_in_trash'    => __('Not found in Trash', 'plugin-name'),
            'featured_image'        => __('Featured Image', 'plugin-name'),
            'set_featured_image'    => __('Set featured image', 'plugin-name'),
            'remove_featured_image' => __('Remove featured image', 'plugin-name'),
            'use_featured_image'    => __('Use as featured image', 'plugin-name'),
            'insert_into_item'      => __('Insert into product', 'plugin-name'),
            'uploaded_to_this_item' => __('Uploaded to this product', 'plugin-name'),
            'items_list'            => __('Products list', 'plugin-name'),
            'items_list_navigation' => __('Products list navigation', 'plugin-name'),
            'filter_items_list'     => __('Filter products list', 'plugin-name'),
        ];

        $args = [
            'label'               => __('Product', 'plugin-name'),
            'description'         => __('Product custom post type', 'plugin-name'),
            'labels'              => $labels,
            'supports'            => ['title', 'editor', 'thumbnail', 'excerpt', 'custom-fields', 'revisions'],
            'taxonomies'          => ['product_category', 'product_tag'],
            'hierarchical'        => false,
            'public'              => true,
            'show_ui'             => true,
            'show_in_menu'        => true,
            'menu_position'       => 20,
            'menu_icon'           => 'dashicons-products',
            'show_in_admin_bar'   => true,
            'show_in_nav_menus'   => true,
            'can_export'          => true,
            'has_archive'         => 'products',
            'exclude_from_search' => false,
            'publicly_queryable'  => true,
            'capability_type'     => 'post',
            'show_in_rest'        => true,  // Enable Gutenberg
            'rest_base'           => 'products',
            'rewrite'             => [
                'slug'       => 'product',
                'with_front' => false,
            ],
            'template'            => [
                ['core/image', ['align' => 'wide']],
                ['core/paragraph', ['placeholder' => 'Product description...']],
            ],
            'template_lock'       => false,  // 'all', 'insert', false
        ];

        register_post_type('product', $args);
    }

    /**
     * Register custom taxonomies
     */
    public function register_taxonomies(): void {
        // Product Category (hierarchical like categories)
        $category_labels = [
            'name'              => _x('Product Categories', 'taxonomy general name', 'plugin-name'),
            'singular_name'     => _x('Product Category', 'taxonomy singular name', 'plugin-name'),
            'search_items'      => __('Search Product Categories', 'plugin-name'),
            'all_items'         => __('All Product Categories', 'plugin-name'),
            'parent_item'       => __('Parent Product Category', 'plugin-name'),
            'parent_item_colon' => __('Parent Product Category:', 'plugin-name'),
            'edit_item'         => __('Edit Product Category', 'plugin-name'),
            'update_item'       => __('Update Product Category', 'plugin-name'),
            'add_new_item'      => __('Add New Product Category', 'plugin-name'),
            'new_item_name'     => __('New Product Category Name', 'plugin-name'),
            'menu_name'         => __('Categories', 'plugin-name'),
        ];

        register_taxonomy('product_category', ['product'], [
            'hierarchical'      => true,
            'labels'            => $category_labels,
            'show_ui'           => true,
            'show_admin_column' => true,
            'query_var'         => true,
            'show_in_rest'      => true,
            'rewrite'           => ['slug' => 'product-category'],
        ]);

        // Product Tags (non-hierarchical like tags)
        $tag_labels = [
            'name'                       => _x('Product Tags', 'taxonomy general name', 'plugin-name'),
            'singular_name'              => _x('Product Tag', 'taxonomy singular name', 'plugin-name'),
            'search_items'               => __('Search Product Tags', 'plugin-name'),
            'popular_items'              => __('Popular Product Tags', 'plugin-name'),
            'all_items'                  => __('All Product Tags', 'plugin-name'),
            'edit_item'                  => __('Edit Product Tag', 'plugin-name'),
            'update_item'                => __('Update Product Tag', 'plugin-name'),
            'add_new_item'               => __('Add New Product Tag', 'plugin-name'),
            'new_item_name'              => __('New Product Tag Name', 'plugin-name'),
            'separate_items_with_commas' => __('Separate tags with commas', 'plugin-name'),
            'add_or_remove_items'        => __('Add or remove tags', 'plugin-name'),
            'choose_from_most_used'      => __('Choose from the most used tags', 'plugin-name'),
            'not_found'                  => __('No tags found.', 'plugin-name'),
            'menu_name'                  => __('Tags', 'plugin-name'),
        ];

        register_taxonomy('product_tag', ['product'], [
            'hierarchical'      => false,
            'labels'            => $tag_labels,
            'show_ui'           => true,
            'show_admin_column' => true,
            'query_var'         => true,
            'show_in_rest'      => true,
            'rewrite'           => ['slug' => 'product-tag'],
        ]);
    }
}
```

---

## Plugin Updates

### Self-Hosted Update Checker

```php
<?php
declare(strict_types=1);

namespace PluginName;

/**
 * Handle plugin updates from custom server
 */
class UpdateChecker {

    private string $plugin_slug;
    private string $update_url;
    private string $plugin_file;

    public function __construct() {
        $this->plugin_slug = 'plugin-name';
        $this->plugin_file = PLUGIN_NAME_BASENAME;
        $this->update_url = 'https://example.com/api/plugin-updates/';
    }

    /**
     * Initialize update checker
     */
    public function init(): void {
        add_filter('pre_set_site_transient_update_plugins', [$this, 'check_for_update']);
        add_filter('plugins_api', [$this, 'plugin_info'], 20, 3);
        add_action('in_plugin_update_message-' . $this->plugin_file, [$this, 'update_message'], 10, 2);
    }

    /**
     * Check for plugin updates
     */
    public function check_for_update(object $transient): object {
        if (empty($transient->checked)) {
            return $transient;
        }

        $remote = $this->get_remote_info();

        if (
            $remote &&
            version_compare(PLUGIN_NAME_VERSION, $remote->version, '<') &&
            version_compare($remote->requires, get_bloginfo('version'), '<=') &&
            version_compare($remote->requires_php, PHP_VERSION, '<=')
        ) {
            $transient->response[$this->plugin_file] = (object) [
                'slug'        => $this->plugin_slug,
                'plugin'      => $this->plugin_file,
                'new_version' => $remote->version,
                'url'         => $remote->url,
                'package'     => $remote->package,
                'icons'       => (array) ($remote->icons ?? []),
                'banners'     => (array) ($remote->banners ?? []),
                'tested'      => $remote->tested ?? '',
                'requires'    => $remote->requires ?? '',
            ];
        }

        return $transient;
    }

    /**
     * Plugin information for update screen
     */
    public function plugin_info(mixed $result, string $action, object $args): mixed {
        if ($action !== 'plugin_information' || $args->slug !== $this->plugin_slug) {
            return $result;
        }

        $remote = $this->get_remote_info();

        if (!$remote) {
            return $result;
        }

        return (object) [
            'name'            => $remote->name,
            'slug'            => $this->plugin_slug,
            'version'         => $remote->version,
            'author'          => $remote->author,
            'author_profile'  => $remote->author_profile ?? '',
            'requires'        => $remote->requires,
            'tested'          => $remote->tested,
            'requires_php'    => $remote->requires_php,
            'sections'        => (array) $remote->sections,
            'download_link'   => $remote->package,
            'banners'         => (array) ($remote->banners ?? []),
            'icons'           => (array) ($remote->icons ?? []),
            'last_updated'    => $remote->last_updated ?? '',
            'homepage'        => $remote->url ?? '',
        ];
    }

    /**
     * Custom update message
     */
    public function update_message(array $plugin_data, object $response): void {
        if (!empty($response->upgrade_notice)) {
            printf(
                '<br /><strong>%s</strong>: %s',
                esc_html__('Upgrade Notice', 'plugin-name'),
                esc_html($response->upgrade_notice)
            );
        }
    }

    /**
     * Get remote plugin information
     */
    private function get_remote_info(): ?object {
        $transient_key = 'plugin_name_update_info';
        $remote = get_transient($transient_key);

        if ($remote !== false) {
            return $remote === 'error' ? null : $remote;
        }

        $response = wp_remote_get($this->update_url . 'info.json', [
            'timeout' => 10,
            'headers' => [
                'Accept' => 'application/json',
            ],
        ]);

        if (
            is_wp_error($response) ||
            wp_remote_retrieve_response_code($response) !== 200 ||
            empty(wp_remote_retrieve_body($response))
        ) {
            set_transient($transient_key, 'error', HOUR_IN_SECONDS);
            return null;
        }

        $remote = json_decode(wp_remote_retrieve_body($response));
        set_transient($transient_key, $remote, 12 * HOUR_IN_SECONDS);

        return $remote;
    }
}
```

---

## Best Practices

### Do

- Use namespaces to avoid function/class name collisions
- Follow WordPress Coding Standards (WPCS)
- Include proper plugin headers with all required fields
- Implement proper activation/deactivation/uninstall hooks
- Use the Settings API for options pages
- Register CPTs with `show_in_rest` for Gutenberg support
- Cache remote API responses with transients
- Provide translation support with text domains
- Include a proper uninstall.php for cleanup

### Do Not

- Access the database directly without proper preparation
- Store options without sanitization
- Skip capability checks in admin functions
- Leave orphaned data after uninstall
- Hardcode plugin paths (use constants)
- Register hooks in constructors (use init methods)
- Modify core WordPress tables
- Include heavy operations in activation hooks

---

## Reference: Theme Development

# Theme Development

---

## Template Hierarchy

WordPress uses a specific hierarchy to determine which template file renders content. Understanding this hierarchy is essential for proper theme development.

### Hierarchy Order (Most Specific to General)

```
1. Custom Template (page-{custom}.php)
2. Specific Template (single-{post-type}-{slug}.php)
3. Type Template (single-{post-type}.php)
4. Archive Template (archive-{post-type}.php)
5. General Template (single.php, archive.php)
6. Index Fallback (index.php)
```

### Complete Template Map

```php
<?php
/**
 * Template hierarchy reference for WordPress 6.4+
 *
 * Homepage:
 *   front-page.php → home.php → index.php
 *
 * Single Post:
 *   single-{post-type}-{slug}.php → single-{post-type}.php → single.php → singular.php → index.php
 *
 * Page:
 *   {custom-template}.php → page-{slug}.php → page-{id}.php → page.php → singular.php → index.php
 *
 * Category:
 *   category-{slug}.php → category-{id}.php → category.php → archive.php → index.php
 *
 * Custom Taxonomy:
 *   taxonomy-{taxonomy}-{term}.php → taxonomy-{taxonomy}.php → taxonomy.php → archive.php → index.php
 *
 * Custom Post Type Archive:
 *   archive-{post-type}.php → archive.php → index.php
 *
 * Author:
 *   author-{nicename}.php → author-{id}.php → author.php → archive.php → index.php
 *
 * Date:
 *   date.php → archive.php → index.php
 *
 * Search:
 *   search.php → index.php
 *
 * 404:
 *   404.php → index.php
 *
 * Attachment:
 *   {mime-type}.php → attachment.php → single-attachment-{slug}.php → single.php → singular.php → index.php
 */
```

---

## Classic Theme Structure

### Minimal Theme Requirements

```
theme-name/
├── style.css          # Required: Theme metadata
├── index.php          # Required: Main template fallback
├── functions.php      # Theme setup and functionality
├── header.php         # Site header
├── footer.php         # Site footer
├── sidebar.php        # Widget area
├── single.php         # Single post template
├── page.php           # Page template
├── archive.php        # Archive template
├── search.php         # Search results
├── 404.php            # Not found page
├── comments.php       # Comment template
├── screenshot.png     # Theme preview (1200x900)
└── assets/
    ├── css/
    ├── js/
    └── images/
```

### style.css Header

```css
/*
Theme Name: Theme Name
Theme URI: https://example.com/theme
Author: Author Name
Author URI: https://example.com
Description: A custom WordPress theme with modern features.
Version: 1.0.0
Requires at least: 6.4
Tested up to: 6.5
Requires PHP: 8.1
License: GNU General Public License v2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html
Text Domain: theme-name
Tags: custom-background, custom-logo, custom-menu, featured-images, threaded-comments
*/
```

### functions.php Setup

```php
<?php
declare(strict_types=1);

/**
 * Theme functions and definitions
 *
 * @package Theme_Name
 * @since 1.0.0
 */

namespace ThemeName;

// Prevent direct access
defined('ABSPATH') || exit;

/**
 * Theme setup
 */
function theme_setup(): void {
    // Make theme translation-ready
    load_theme_textdomain('theme-name', get_template_directory() . '/languages');

    // Add default posts and comments RSS feed links
    add_theme_support('automatic-feed-links');

    // Let WordPress manage the document title
    add_theme_support('title-tag');

    // Enable featured images
    add_theme_support('post-thumbnails');
    add_image_size('theme-featured', 1200, 630, true);
    add_image_size('theme-card', 600, 400, true);

    // Register navigation menus
    register_nav_menus([
        'primary'   => esc_html__('Primary Menu', 'theme-name'),
        'footer'    => esc_html__('Footer Menu', 'theme-name'),
        'mobile'    => esc_html__('Mobile Menu', 'theme-name'),
    ]);

    // Switch to HTML5 markup
    add_theme_support('html5', [
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
        'style',
        'script',
        'navigation-widgets',
    ]);

    // Enable selective refresh for widgets
    add_theme_support('customize-selective-refresh-widgets');

    // Add custom logo support
    add_theme_support('custom-logo', [
        'height'      => 100,
        'width'       => 400,
        'flex-height' => true,
        'flex-width'  => true,
    ]);

    // Add responsive embed support
    add_theme_support('responsive-embeds');

    // Add editor styles
    add_theme_support('editor-styles');
    add_editor_style('assets/css/editor-style.css');

    // Wide and full alignment support
    add_theme_support('align-wide');

    // Block styles
    add_theme_support('wp-block-styles');
}
add_action('after_setup_theme', __NAMESPACE__ . '\\theme_setup');

/**
 * Enqueue scripts and styles
 */
function enqueue_assets(): void {
    $theme_version = wp_get_theme()->get('Version');
    $assets_path = get_template_directory() . '/assets';
    $assets_uri = get_template_directory_uri() . '/assets';

    // Main stylesheet
    wp_enqueue_style(
        'theme-name-style',
        $assets_uri . '/css/main.css',
        [],
        filemtime($assets_path . '/css/main.css')
    );

    // Main JavaScript
    wp_enqueue_script(
        'theme-name-script',
        $assets_uri . '/js/main.js',
        [],
        filemtime($assets_path . '/js/main.js'),
        true
    );

    // Localize script with data
    wp_localize_script('theme-name-script', 'themeNameData', [
        'ajaxUrl' => admin_url('admin-ajax.php'),
        'nonce'   => wp_create_nonce('theme_name_nonce'),
        'homeUrl' => home_url('/'),
    ]);

    // Comment reply script
    if (is_singular() && comments_open() && get_option('thread_comments')) {
        wp_enqueue_script('comment-reply');
    }
}
add_action('wp_enqueue_scripts', __NAMESPACE__ . '\\enqueue_assets');

/**
 * Register widget areas
 */
function register_sidebars(): void {
    register_sidebar([
        'name'          => esc_html__('Main Sidebar', 'theme-name'),
        'id'            => 'sidebar-main',
        'description'   => esc_html__('Add widgets here.', 'theme-name'),
        'before_widget' => '<section id="%1$s" class="widget %2$s">',
        'after_widget'  => '</section>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ]);

    register_sidebar([
        'name'          => esc_html__('Footer Widgets', 'theme-name'),
        'id'            => 'sidebar-footer',
        'description'   => esc_html__('Footer widget area.', 'theme-name'),
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h4 class="widget-title">',
        'after_title'   => '</h4>',
    ]);
}
add_action('widgets_init', __NAMESPACE__ . '\\register_sidebars');

/**
 * Set content width
 */
function set_content_width(): void {
    $GLOBALS['content_width'] = apply_filters('theme_name_content_width', 1200);
}
add_action('after_setup_theme', __NAMESPACE__ . '\\set_content_width', 0);
```

---

## Child Theme Development

### When to Use Child Themes

**Use Child Themes When:**
- Customizing an existing theme
- Making CSS modifications to a parent theme
- Overriding specific template files
- Adding functionality without modifying parent theme

**Use Custom Themes When:**
- Building from scratch
- Significant structural changes needed
- Different design system requirements

### Child Theme Structure

```
theme-name-child/
├── style.css          # Required: Child theme metadata
├── functions.php      # Child theme functions
├── screenshot.png     # Child theme preview
└── templates/         # Template overrides
    └── parts/
```

### Child Theme style.css

```css
/*
Theme Name: Theme Name Child
Theme URI: https://example.com/theme-child
Description: Child theme for Theme Name
Author: Author Name
Author URI: https://example.com
Template: theme-name
Version: 1.0.0
Requires at least: 6.4
Tested up to: 6.5
Requires PHP: 8.1
License: GNU General Public License v2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html
Text Domain: theme-name-child
*/

/* Child theme styles below */
```

### Child Theme functions.php

```php
<?php
declare(strict_types=1);

/**
 * Child theme functions
 *
 * @package Theme_Name_Child
 */

namespace ThemeNameChild;

defined('ABSPATH') || exit;

/**
 * Enqueue parent and child theme styles
 */
function enqueue_styles(): void {
    $parent_style = 'theme-name-style';

    // Enqueue parent theme stylesheet
    wp_enqueue_style(
        $parent_style,
        get_template_directory_uri() . '/assets/css/main.css',
        [],
        wp_get_theme()->parent()->get('Version')
    );

    // Enqueue child theme stylesheet
    wp_enqueue_style(
        'theme-name-child-style',
        get_stylesheet_uri(),
        [$parent_style],
        wp_get_theme()->get('Version')
    );
}
add_action('wp_enqueue_scripts', __NAMESPACE__ . '\\enqueue_styles');

/**
 * Override parent theme functions as needed
 */
```

---

## Block Theme Development (FSE)

WordPress 6.4+ fully supports Full Site Editing with block themes.

### Block Theme Structure

```
block-theme/
├── style.css              # Theme metadata
├── theme.json             # Global settings and styles
├── functions.php          # Theme functions (minimal for block themes)
├── templates/             # Block templates (HTML)
│   ├── index.html         # Required: Main fallback
│   ├── front-page.html    # Homepage
│   ├── single.html        # Single posts
│   ├── page.html          # Pages
│   ├── archive.html       # Archives
│   ├── search.html        # Search results
│   └── 404.html           # Not found
├── parts/                 # Template parts
│   ├── header.html
│   ├── footer.html
│   └── sidebar.html
├── patterns/              # Block patterns
│   └── hero-section.php
└── assets/
    ├── fonts/
    └── images/
```

### theme.json (WordPress 6.4+)

```json
{
    "$schema": "https://schemas.wp.org/trunk/theme.json",
    "version": 3,
    "settings": {
        "appearanceTools": true,
        "useRootPaddingAwareAlignments": true,
        "layout": {
            "contentSize": "800px",
            "wideSize": "1200px"
        },
        "color": {
            "defaultDuotone": false,
            "defaultGradients": false,
            "defaultPalette": false,
            "palette": [
                {
                    "color": "#1a1a2e",
                    "name": "Primary",
                    "slug": "primary"
                },
                {
                    "color": "#16213e",
                    "name": "Secondary",
                    "slug": "secondary"
                },
                {
                    "color": "#0f3460",
                    "name": "Accent",
                    "slug": "accent"
                },
                {
                    "color": "#e94560",
                    "name": "Highlight",
                    "slug": "highlight"
                },
                {
                    "color": "#ffffff",
                    "name": "Base",
                    "slug": "base"
                },
                {
                    "color": "#f8f9fa",
                    "name": "Base Alt",
                    "slug": "base-alt"
                }
            ]
        },
        "typography": {
            "fluid": true,
            "fontFamilies": [
                {
                    "fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen-Sans, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif",
                    "name": "System Font",
                    "slug": "system"
                },
                {
                    "fontFamily": "'Inter', sans-serif",
                    "fontFace": [
                        {
                            "fontFamily": "Inter",
                            "fontWeight": "400",
                            "fontStyle": "normal",
                            "src": ["file:./assets/fonts/inter-regular.woff2"]
                        },
                        {
                            "fontFamily": "Inter",
                            "fontWeight": "600",
                            "fontStyle": "normal",
                            "src": ["file:./assets/fonts/inter-semibold.woff2"]
                        },
                        {
                            "fontFamily": "Inter",
                            "fontWeight": "700",
                            "fontStyle": "normal",
                            "src": ["file:./assets/fonts/inter-bold.woff2"]
                        }
                    ],
                    "name": "Inter",
                    "slug": "inter"
                }
            ],
            "fontSizes": [
                {
                    "fluid": {
                        "min": "0.875rem",
                        "max": "1rem"
                    },
                    "name": "Small",
                    "size": "1rem",
                    "slug": "small"
                },
                {
                    "fluid": {
                        "min": "1rem",
                        "max": "1.125rem"
                    },
                    "name": "Medium",
                    "size": "1.125rem",
                    "slug": "medium"
                },
                {
                    "fluid": {
                        "min": "1.25rem",
                        "max": "1.5rem"
                    },
                    "name": "Large",
                    "size": "1.5rem",
                    "slug": "large"
                },
                {
                    "fluid": {
                        "min": "1.75rem",
                        "max": "2.25rem"
                    },
                    "name": "Extra Large",
                    "size": "2.25rem",
                    "slug": "x-large"
                },
                {
                    "fluid": {
                        "min": "2.5rem",
                        "max": "3.5rem"
                    },
                    "name": "Huge",
                    "size": "3.5rem",
                    "slug": "huge"
                }
            ]
        },
        "spacing": {
            "spacingScale": {
                "steps": 7
            },
            "spacingSizes": [
                {
                    "name": "XS",
                    "size": "0.5rem",
                    "slug": "xs"
                },
                {
                    "name": "S",
                    "size": "1rem",
                    "slug": "s"
                },
                {
                    "name": "M",
                    "size": "1.5rem",
                    "slug": "m"
                },
                {
                    "name": "L",
                    "size": "2rem",
                    "slug": "l"
                },
                {
                    "name": "XL",
                    "size": "3rem",
                    "slug": "xl"
                },
                {
                    "name": "XXL",
                    "size": "4rem",
                    "slug": "xxl"
                }
            ],
            "units": ["%", "px", "em", "rem", "vh", "vw"]
        },
        "blocks": {
            "core/button": {
                "border": {
                    "radius": true
                }
            },
            "core/pullquote": {
                "border": {
                    "color": true,
                    "radius": true,
                    "style": true,
                    "width": true
                }
            }
        }
    },
    "styles": {
        "color": {
            "background": "var(--wp--preset--color--base)",
            "text": "var(--wp--preset--color--primary)"
        },
        "typography": {
            "fontFamily": "var(--wp--preset--font-family--system)",
            "fontSize": "var(--wp--preset--font-size--medium)",
            "lineHeight": "1.6"
        },
        "spacing": {
            "padding": {
                "top": "var(--wp--preset--spacing--m)",
                "right": "var(--wp--preset--spacing--m)",
                "bottom": "var(--wp--preset--spacing--m)",
                "left": "var(--wp--preset--spacing--m)"
            }
        },
        "elements": {
            "link": {
                "color": {
                    "text": "var(--wp--preset--color--accent)"
                },
                ":hover": {
                    "color": {
                        "text": "var(--wp--preset--color--highlight)"
                    }
                }
            },
            "button": {
                "border": {
                    "radius": "4px"
                },
                "color": {
                    "background": "var(--wp--preset--color--accent)",
                    "text": "var(--wp--preset--color--base)"
                },
                ":hover": {
                    "color": {
                        "background": "var(--wp--preset--color--highlight)"
                    }
                }
            },
            "heading": {
                "typography": {
                    "fontFamily": "var(--wp--preset--font-family--inter)",
                    "fontWeight": "700",
                    "lineHeight": "1.2"
                }
            },
            "h1": {
                "typography": {
                    "fontSize": "var(--wp--preset--font-size--huge)"
                }
            },
            "h2": {
                "typography": {
                    "fontSize": "var(--wp--preset--font-size--x-large)"
                }
            }
        },
        "blocks": {
            "core/site-title": {
                "typography": {
                    "fontFamily": "var(--wp--preset--font-family--inter)",
                    "fontSize": "var(--wp--preset--font-size--large)",
                    "fontWeight": "700"
                }
            },
            "core/navigation": {
                "typography": {
                    "fontSize": "var(--wp--preset--font-size--small)"
                }
            }
        }
    },
    "templateParts": [
        {
            "area": "header",
            "name": "header",
            "title": "Header"
        },
        {
            "area": "footer",
            "name": "footer",
            "title": "Footer"
        },
        {
            "area": "uncategorized",
            "name": "sidebar",
            "title": "Sidebar"
        }
    ],
    "customTemplates": [
        {
            "name": "blank",
            "postTypes": ["page", "post"],
            "title": "Blank"
        },
        {
            "name": "full-width",
            "postTypes": ["page"],
            "title": "Full Width"
        }
    ]
}
```

### Block Template Example (templates/single.html)

```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->

<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group">
    <!-- wp:post-featured-image {"align":"wide"} /-->

    <!-- wp:group {"style":{"spacing":{"margin":{"top":"var:preset|spacing|l"}}}} -->
    <div class="wp-block-group">
        <!-- wp:post-title {"level":1} /-->

        <!-- wp:group {"layout":{"type":"flex","flexWrap":"nowrap"},"style":{"spacing":{"blockGap":"var:preset|spacing|s"}}} -->
        <div class="wp-block-group">
            <!-- wp:post-date /-->
            <!-- wp:post-author {"showAvatar":false} /-->
            <!-- wp:post-terms {"term":"category"} /-->
        </div>
        <!-- /wp:group -->
    </div>
    <!-- /wp:group -->

    <!-- wp:post-content {"layout":{"type":"constrained"}} /-->

    <!-- wp:post-terms {"term":"post_tag","prefix":"Tags: "} /-->

    <!-- wp:comments {"className":"wp-block-comments-query-loop"} -->
    <div class="wp-block-comments wp-block-comments-query-loop">
        <!-- wp:comments-title /-->
        <!-- wp:comment-template -->
            <!-- wp:group {"style":{"spacing":{"margin":{"bottom":"var:preset|spacing|m"}}}} -->
            <div class="wp-block-group">
                <!-- wp:group {"layout":{"type":"flex","flexWrap":"nowrap"}} -->
                <div class="wp-block-group">
                    <!-- wp:avatar {"size":48} /-->
                    <!-- wp:comment-author-name /-->
                    <!-- wp:comment-date /-->
                </div>
                <!-- /wp:group -->
                <!-- wp:comment-content /-->
                <!-- wp:comment-reply-link /-->
            </div>
            <!-- /wp:group -->
        <!-- /wp:comment-template -->
        <!-- wp:comments-pagination -->
            <!-- wp:comments-pagination-previous /-->
            <!-- wp:comments-pagination-numbers /-->
            <!-- wp:comments-pagination-next /-->
        <!-- /wp:comments-pagination -->
        <!-- wp:post-comments-form /-->
    </div>
    <!-- /wp:comments -->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

### Template Part Example (parts/header.html)

```html
<!-- wp:group {"tagName":"header","className":"site-header","layout":{"type":"constrained"},"style":{"spacing":{"padding":{"top":"var:preset|spacing|m","bottom":"var:preset|spacing|m"}}}} -->
<header class="wp-block-group site-header">
    <!-- wp:group {"layout":{"type":"flex","justifyContent":"space-between","flexWrap":"wrap"}} -->
    <div class="wp-block-group">
        <!-- wp:group {"layout":{"type":"flex","flexWrap":"nowrap"}} -->
        <div class="wp-block-group">
            <!-- wp:site-logo {"width":50} /-->
            <!-- wp:site-title /-->
        </div>
        <!-- /wp:group -->

        <!-- wp:navigation {"ref":123,"layout":{"type":"flex","setCascadingProperties":true},"style":{"spacing":{"blockGap":"var:preset|spacing|m"}}} /-->
    </div>
    <!-- /wp:group -->
</header>
<!-- /wp:group -->
```

---

## Block Patterns

### Registering Block Patterns

```php
<?php
/**
 * patterns/hero-section.php
 *
 * Title: Hero Section
 * Slug: theme-name/hero-section
 * Categories: featured, banner
 * Keywords: hero, banner, call to action
 * Block Types: core/template-part/header
 * Viewport Width: 1400
 */

declare(strict_types=1);

defined('ABSPATH') || exit;
?>

<!-- wp:cover {"url":"<?php echo esc_url(get_template_directory_uri()); ?>/assets/images/hero-bg.jpg","dimRatio":60,"overlayColor":"primary","align":"full","style":{"spacing":{"padding":{"top":"var:preset|spacing|xxl","bottom":"var:preset|spacing|xxl"}}}} -->
<div class="wp-block-cover alignfull">
    <span aria-hidden="true" class="wp-block-cover__background has-primary-background-color has-background-dim-60 has-background-dim"></span>
    <img class="wp-block-cover__image-background" src="<?php echo esc_url(get_template_directory_uri()); ?>/assets/images/hero-bg.jpg" alt="" />
    <div class="wp-block-cover__inner-container">
        <!-- wp:group {"layout":{"type":"constrained"}} -->
        <div class="wp-block-group">
            <!-- wp:heading {"textAlign":"center","level":1,"textColor":"base","fontSize":"huge"} -->
            <h1 class="wp-block-heading has-text-align-center has-base-color has-text-color has-huge-font-size"><?php esc_html_e('Welcome to Our Site', 'theme-name'); ?></h1>
            <!-- /wp:heading -->

            <!-- wp:paragraph {"align":"center","textColor":"base","fontSize":"large"} -->
            <p class="has-text-align-center has-base-color has-text-color has-large-font-size"><?php esc_html_e('Discover amazing content and features that will help you succeed.', 'theme-name'); ?></p>
            <!-- /wp:paragraph -->

            <!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
            <div class="wp-block-buttons">
                <!-- wp:button {"backgroundColor":"highlight","textColor":"base"} -->
                <div class="wp-block-button"><a class="wp-block-button__link has-base-color has-highlight-background-color has-text-color has-background wp-element-button"><?php esc_html_e('Get Started', 'theme-name'); ?></a></div>
                <!-- /wp:button -->

                <!-- wp:button {"className":"is-style-outline"} -->
                <div class="wp-block-button is-style-outline"><a class="wp-block-button__link wp-element-button"><?php esc_html_e('Learn More', 'theme-name'); ?></a></div>
                <!-- /wp:button -->
            </div>
            <!-- /wp:buttons -->
        </div>
        <!-- /wp:group -->
    </div>
</div>
<!-- /wp:cover -->
```

### Registering Patterns in functions.php

```php
<?php
/**
 * Register block pattern categories
 */
function register_pattern_categories(): void {
    register_block_pattern_category('theme-name-patterns', [
        'label' => __('Theme Name Patterns', 'theme-name'),
    ]);
}
add_action('init', __NAMESPACE__ . '\\register_pattern_categories');
```

---

## Best Practices

### Do

- Use `theme.json` for all design tokens in block themes
- Leverage fluid typography for responsive text
- Create reusable template parts for header/footer
- Register block patterns for common layouts
- Use CSS custom properties from `theme.json`
- Implement proper accessibility (skip links, ARIA)
- Test in the Site Editor and frontend

### Do Not

- Mix classic theme files with block theme templates
- Hardcode colors or sizes in templates
- Skip the `$schema` property in `theme.json`
- Ignore mobile responsiveness in patterns
- Override core block styles excessively
- Forget to escape translatable strings in patterns
