# Design System

Textual design system 由很多预定义颜色，和如何使用它们的 guidelines 构成。

这些 guidelines 不是必须遵守的，但是遵守它们可以让内置 widgets，第三方 widgets，以及你自己创建的 widgets 外观保持一致，而不需要担心颜色冲突。

Textual 的颜色系统是基于 Google Material design system 的，并对它们进行调整以适应 terminal。

## Designing with Colors

Textual 以 CSS 变量预定义大量颜色。例如 CSS 变量 $primary 被设置为 #004578（header 使用的 blue）。

```css
MyWidget {
    background: $primary;
    color: $text;
}
```

使用变量而不是明确的颜色，允许 Textual 应用 color themes。Textual 支持一个默认的 light 和 dark theme，但是将来可能有更多可用的 themes，因此应尽量使用 CSS 变量。

### Base Colors

color scheme 定义了 12 个基本颜色。下面的列表列出了每个颜色的名字和在哪里使用它们：

| Color Variable | Description |
| --- | --- |
| $primary | primary 颜色，可以被考虑为 branding color。通常用于 titles，backgrounds，用以重点强调 |
| $secondary | branding color 的代替颜色，和 $primary 有相似的目的，用于从 primary color 区分一些东西 |
| $primary-background | 应用到 background 的 primary color。在 light mode，它就是 $primary。在 dark mode，它就是 $primary 的 dimmed version |
| $secondary-background | 应用到 background 的 secondary color。在 light mode，它就是 $secondary。在 dar mode，它就是 $secondary 的 dimmed version |
| $background | 用于没有 content 的 background |
| $surface | 用于 text 下面的 color |
| $panel | 用以区分构成 main content 的部分 UI，通常用于 dialogs 或 sidebars |
| $boost | 带有 alpha 的颜色，可以用于在 background 上创建 layers |
| $warning | 指示一个 warning。Text 或 background |
| $error | 指示一个 error。Text 或 background |
| $success | 指示一个 success。Text 或 background |
| $accent | 用于轻微绘制 UI 上的一部分以吸引注意力，典型地就是 focused widgets 的 border |
| | |

### Shades

对每个 color，Textual 产生 3 个 dark shades 和 3 个 light shades：

- 添加 -lighten-1, -lighten-2, -lighten-3 到 color variable name，就可以得到更 lighter shades（3 是最亮的）
- 添加 -darken-1, -darken-2, -darken-3 到 color variable name，就可以得到更 darker shades（3 是最暗的）

### Dark mode

Textual 内置了两个 color themes，light mode 和 dark mode。可以通过 toggle app.dark 属性来切换它们。

在 dark mode，$background 和 $surface 是 off-black。Dark mode 还设置 $primary-background 和 $secondary-background 为 $primary 和 $secondary 的 dark versions。

### Text color

Design system 定义 3 个 CSS variables，应该将它们用于 text color：

- $text 设置 app 中的 text 颜色。App 中绝大多数 text 应该使用这个颜色
- $text-mute 设置 text color 的轻微 faded 版本。将它用于不是那么重要的 text，例如 sub-title，或者补充信息
- $text-disabled 设置 faded out text，指示它已经被 disabled。例如不可用不可点击的 menu items 或 button 的 text

可以通过 color 属性设置这些颜色。Design system 对 text 使用 auto colors，这意味着 Textual 会 pcik white 或 black，看哪个能提高更好的对比度。

这些 text colors 都应用了一些 alpha。因此即使 $text 也不是纯粹的 white 或 black。这是因为将 text 和 background 混合一点可以避免太刺眼。

### Theming

在将来的 Textual 版本中，可以直接修改 theme 的 colors，并允许用户配置喜欢的 themes。

## Color Preview

textual colors 可以预览 color system 定义的颜色。

