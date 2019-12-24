## Markdown 中使用 LaTeX 添加数学公式
发表于 2019-02-27 更新于 2019-04-22

在 Markdown 文件中使用 LaTeX 来添加数学公式非常简单。

## [](#环境搭建 "环境搭建")环境搭建

*   **编辑环境**：需要一个支持渲染 LaTeX 公式的编辑器，macOS 下推荐使用 [Typora](https://typora.io/)，使用了`MathJax` 渲染引擎，对 LaTeX 语法基本上支持的很全面。详情可见[Typora/Math](https://support.typora.io/Math/)。
*   **Hexo 页面生成**：[Hexo](https://hexo.io/zh-cn/) 中一些主题（例如：[NexT](https://theme-next.org/docs/third-party-services/math-equations/) ）可以使用 MathJax 来渲染数学公式。NexT 主题开启数学公式渲染功能，[参考链接](https://theme-next.org/docs/third-party-services/math-equations/)。下面以 NexT 主题为例：

1.  修改 `next/_config.yml` 文件中的 `math` 字段。

<div class="highlight-wrap">

<figure class="highlight yaml">

<div class="table-container">

<table>

<tbody>

<tr>

<td class="gutter">

<pre><span class="line">1</span>  
<span class="line">2</span>  
<span class="line">3</span>  
</pre>

</td>

<td class="code">

<pre><span class="line"><span class="attr">math:</span> <span class="literal">true</span> <span class="comment"># true 表示开启数学公式渲染</span></span>  
<span class="line"> <span class="attr">per_page:</span> <span class="literal">true</span> <span class="comment"># true 表示单独页面设置</span></span>  
<span class="line"> <span class="attr">engine:</span> <span class="string">mathjax</span> <span class="comment"># 渲染引擎，推荐mathjax</span></span>  
</pre>

</td>

</tr>

</tbody>

</table>

</div>

</figure>

<div class="copy-btn">复制</div>

</div>

1.  如果 `per_page` 字段为 `true`，还需要在 `md` 文件的页头处加入 `mathjax: true` 字段。

<div class="highlight-wrap">

<figure class="highlight yaml">

<div class="table-container">

<table>

<tbody>

<tr>

<td class="gutter">

<pre><span class="line">1</span>  
<span class="line">2</span>  
<span class="line">3</span>  
<span class="line">4</span>  
<span class="line">5</span>  
</pre>

</td>

<td class="code">

<pre><span class="line"><span class="meta">---</span></span>  
<span class="line"><span class="attr">title:</span> <span class="string">XXX</span></span>  
<span class="line"><span class="attr">tags:</span> <span class="string">tags</span></span>  
<span class="line"><span class="attr">mathjax:</span> <span class="literal">true</span></span>  
<span class="line"><span class="meta">---</span></span>  
</pre>

</td>

</tr>

</tbody>

</table>

</div>

</figure>

<div class="copy-btn">复制</div>

</div>

## [](#在-Markdown-中添加公式 "在 Markdown 中添加公式")在 Markdown 中添加公式

### [](#行内公式 "行内公式")行内公式

在 LaTeX 语法公式前后加上 $ 。例如：

这是一个公式 <span class="MathJax_Preview" style="color: inherit;"></span><span class="MathJax" id="MathJax-Element-1-Frame" tabindex="0" style="position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-1" style="width: 5.342em; display: inline-block;"><span style="display: inline-block; position: relative; width: 4.134em; height: 0px; font-size: 129%;"><span style="position: absolute; clip: rect(1.533em, 1004.13em, 2.903em, -1000em); top: -2.412em; left: 0em;"><span class="mrow" id="MathJax-Span-2"><span class="mi" id="MathJax-Span-3" style="font-family: MathJax_Math-italic;">f<span style="display: inline-block; overflow: hidden; height: 1px; width: 0.06em;"></span></span><span class="mo" id="MathJax-Span-4" style="font-family: MathJax_Main;">(</span><span class="mi" id="MathJax-Span-5" style="font-family: MathJax_Math-italic;">r</span><span class="mo" id="MathJax-Span-6" style="font-family: MathJax_Main;">)</span><span class="mo" id="MathJax-Span-7" style="font-family: MathJax_Main; padding-left: 0.278em;">=</span><span class="mfrac" id="MathJax-Span-8" style="padding-left: 0.278em;"><span style="display: inline-block; position: relative; width: 0.844em; height: 0px; margin-right: 0.12em; margin-left: 0.12em;"><span style="position: absolute; clip: rect(3.563em, 1000.71em, 4.142em, -1000em); top: -4.404em; left: 50%; margin-left: -0.362em;"><span class="mrow" id="MathJax-Span-9"><span class="mi" id="MathJax-Span-10" style="font-size: 70.7%; font-family: MathJax_Math-italic;">π<span style="display: inline-block; overflow: hidden; height: 1px; width: 0.002em;"></span></span><span class="mi" id="MathJax-Span-11" style="font-size: 70.7%; font-family: MathJax_Math-italic;">r</span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; clip: rect(3.405em, 1000.32em, 4.134em, -1000em); top: -3.643em; left: 50%; margin-left: -0.177em;"><span class="mn" id="MathJax-Span-12" style="font-size: 70.7%; font-family: MathJax_Main;">2</span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; clip: rect(0.887em, 1000.84em, 1.206em, -1000em); top: -1.297em; left: 0em;"><span style="display: inline-block; overflow: hidden; vertical-align: 0em; border-top: 1.4px solid; width: 0.844em; height: 0px;"></span><span style="display: inline-block; width: 0px; height: 1.077em;"></span></span></span></span></span><span style="display: inline-block; width: 0px; height: 2.412em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.522em; border-left: 0px solid; width: 0px; height: 1.545em;"></span></span></nobr><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>f</mi><mo stretchy="false">(</mo><mi>r</mi><mo stretchy="false">)</mo><mo>=</mo><mfrac><mrow><mi>π</mi><mi>r</mi></mrow><mn>2</mn></mfrac></math></span><mi>f</mi><mo stretchy=&quot;false&quot;>(</mo><mi>r</mi><mo stretchy=&quot;false&quot;>)</mo><mo>=</mo><mfrac><mrow><mi>&amp;#x03C0;</mi><mi>r</mi></mrow><mn>2</mn></mfrac></math>" role="presentation"></span> <script type="math/tex" id="MathJax-Element-1">f(r) = \frac {\pi r} {2}</script>

<div class="highlight-wrap">

<figure class="highlight plain">

<div class="table-container">

<table>

<tbody>

<tr>

<td class="gutter">

<pre><span class="line">1</span>  
</pre>

</td>

<td class="code">

<pre><span class="line">这是一个公式 $f(r) = \frac {\pi r} {2} $</span>  
</pre>

</td>

</tr>

</tbody>

</table>

</div>

</figure>

<div class="copy-btn">复制</div>

</div>

<a id="more"></a>

### [](#行间公式（公式块） "行间公式（公式块）")行间公式（公式块）

在 LaTeX 语法公式前后行加上 $。例如：

<span class="MathJax_Preview" style="color: inherit;"></span>

<div class="MathJax_Display has-jax" style="text-align: center;"><span class="MathJax" id="MathJax-Element-2-Frame" tabindex="0" style="text-align: center; position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot; display=&quot;block&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-13" style="width: 5.73em; display: inline-block;"><span style="display: inline-block; position: relative; width: 4.436em; height: 0px; font-size: 129%;"><span style="position: absolute; clip: rect(1.164em, 1004.44em, 3.227em, -1000em); top: -2.412em; left: 0em;"><span class="mrow" id="MathJax-Span-14"><span class="mi" id="MathJax-Span-15" style="font-family: MathJax_Math-italic;">f<span style="display: inline-block; overflow: hidden; height: 1px; width: 0.06em;"></span></span><span class="mo" id="MathJax-Span-16" style="font-family: MathJax_Main;">(</span><span class="mi" id="MathJax-Span-17" style="font-family: MathJax_Math-italic;">r</span><span class="mo" id="MathJax-Span-18" style="font-family: MathJax_Main;">)</span><span class="mo" id="MathJax-Span-19" style="font-family: MathJax_Main; padding-left: 0.278em;">=</span><span class="mfrac" id="MathJax-Span-20" style="padding-left: 0.278em;"><span style="display: inline-block; position: relative; width: 1.144em; height: 0px; margin-right: 0.12em; margin-left: 0.12em;"><span style="position: absolute; clip: rect(3.434em, 1001em, 4.145em, -1000em); top: -4.682em; left: 50%; margin-left: -0.512em;"><span class="mrow" id="MathJax-Span-21"><span class="mi" id="MathJax-Span-22" style="font-family: MathJax_Math-italic;">π<span style="display: inline-block; overflow: hidden; height: 1px; width: 0.003em;"></span></span><span class="mi" id="MathJax-Span-23" style="font-family: MathJax_Math-italic;">r</span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; clip: rect(3.21em, 1000.45em, 4.134em, -1000em); top: -3.319em; left: 50%; margin-left: -0.25em;"><span class="mn" id="MathJax-Span-24" style="font-family: MathJax_Main;">2</span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; clip: rect(0.887em, 1001.14em, 1.206em, -1000em); top: -1.297em; left: 0em;"><span style="display: inline-block; overflow: hidden; vertical-align: 0em; border-top: 1.4px solid; width: 1.144em; height: 0px;"></span><span style="display: inline-block; width: 0px; height: 1.077em;"></span></span></span></span></span><span style="display: inline-block; width: 0px; height: 2.412em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.94em; border-left: 0px solid; width: 0px; height: 2.439em;"></span></span></nobr><span class="MJX_Assistive_MathML MJX_Assistive_MathML_Block" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mi>f</mi><mo stretchy="false">(</mo><mi>r</mi><mo stretchy="false">)</mo><mo>=</mo><mfrac><mrow><mi>π</mi><mi>r</mi></mrow><mn>2</mn></mfrac></math></span><mi>f</mi><mo stretchy=&quot;false&quot;>(</mo><mi>r</mi><mo stretchy=&quot;false&quot;>)</mo><mo>=</mo><mfrac><mrow><mi>&amp;#x03C0;</mi><mi>r</mi></mrow><mn>2</mn></mfrac></math>" role="presentation"></span></div>

<script type="math/tex; mode=display" id="MathJax-Element-2">\begin{equation*} f(r) = \frac {\pi r} {2} \end{equation*}</script>

<div class="highlight-wrap">

<figure class="highlight tex">

<div class="table-container">

<table>

<tbody>

<tr>

<td class="gutter">

<pre><span class="line">1</span>  
<span class="line">2</span>  
<span class="line">3</span>  
</pre>

</td>

<td class="code">

<pre><span class="line"><span class="formula">$</span></span>  
<span class="line"><span class="formula">f(r) = <span class="tag">\<span class="name">frac</span></span> {<span class="tag">\<span class="name">pi</span></span> r} {2}</span></span>  
<span class="line"><span class="formula">$</span></span>  
</pre>

</td>

</tr>

</tbody>

</table>

</div>

</figure>

<div class="copy-btn">复制</div>

</div>

### [](#添加数字索引 "添加数字索引")添加数字索引

在行间公式中添加 `\begin{equation}...\end{equation}`。例如：

<span class="MathJax_Preview" style="color: inherit;"></span>

<div class="MathJax_Display has-jax"><span class="MathJax MathJax_FullWidth" id="MathJax-Element-3-Frame" tabindex="0" style="position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot; display=&quot;block&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-25" style="width: 100%; display: inline-block; min-width: 8.391em;"><span style="display: inline-block; position: relative; width: 100%; height: 0px; font-size: 129%; min-width: 8.391em;"><span style="position: absolute; clip: rect(3.059em, 1004.24em, 4.451em, -1000em); top: -4.005em; left: 0em; width: 100%;"><span class="mrow" id="MathJax-Span-26"><span class="mtable" id="MathJax-Span-27" style="min-width: 8.391em;"><span style="display: inline-block; position: relative; width: 100%; height: 0px; min-width: 8.391em;"><span style="display: inline-block; position: absolute; width: 4.235em; height: 0px; clip: rect(-0.946em, 1004.24em, 0.446em, -1000em); top: 0em; left: 50%; margin-left: -2.117em;"><span style="position: absolute; clip: rect(3.059em, 1004.24em, 4.451em, -1000em); top: -4.005em; left: 0em;"><span style="display: inline-block; position: relative; width: 4.235em; height: 0px;"><span style="position: absolute; clip: rect(2.992em, 1004.24em, 4.384em, -1000em); top: -3.938em; left: 50%; margin-left: -2.117em;"><span class="mtd" id="MathJax-Span-31"><span class="mrow" id="MathJax-Span-32"><span class="mi" id="MathJax-Span-33" style="font-family: MathJax_Math-italic;">f<span style="display: inline-block; overflow: hidden; height: 1px; width: 0.06em;"></span></span><span class="mo" id="MathJax-Span-34" style="font-family: MathJax_Main;">(</span><span class="mi" id="MathJax-Span-35" style="font-family: MathJax_Math-italic;">x</span><span class="mo" id="MathJax-Span-36" style="font-family: MathJax_Main;">)</span><span class="mo" id="MathJax-Span-37" style="font-family: MathJax_Main; padding-left: 0.278em;">=</span><span class="msubsup" id="MathJax-Span-38" style="padding-left: 0.278em;"><span style="display: inline-block; position: relative; width: 1.001em; height: 0px;"><span style="position: absolute; clip: rect(3.434em, 1000.52em, 4.145em, -1000em); top: -4.005em; left: 0em;"><span class="mi" id="MathJax-Span-39" style="font-family: MathJax_Math-italic;">x</span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; top: -4.418em; left: 0.572em;"><span class="mn" id="MathJax-Span-40" style="font-size: 70.7%; font-family: MathJax_Main;">2</span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span></span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span><span style="display: inline-block; position: absolute; width: 1.278em; height: 0px; clip: rect(-0.812em, 1001.18em, 0.446em, -1000em); top: 0em; right: 0em; margin-right: 0em;"><span style="position: absolute; clip: rect(3.126em, 1001.18em, 4.384em, -1000em); top: -3.938em; right: 0em;"><span class="mtd" id="mjx-eqn-1"><span class="mrow" id="MathJax-Span-29"><span class="mtext" id="MathJax-Span-30" style="font-family: MathJax_Main;">(1)</span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span></span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.464em; border-left: 0px solid; width: 0px; height: 1.574em;"></span></span></nobr><span class="MJX_Assistive_MathML MJX_Assistive_MathML_Block" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mtable displaystyle="true"><mlabeledtr><mtd id="mjx-eqn-1"><mtext>(1)</mtext></mtd><mtd><mi>f</mi><mo stretchy="false">(</mo><mi>x</mi><mo stretchy="false">)</mo><mo>=</mo><msup><mi>x</mi><mn>2</mn></msup></mtd></mlabeledtr></mtable></math></span><mtable displaystyle=&quot;true&quot;><mlabeledtr><mtd id=&quot;mjx-eqn-1&quot;><mtext>(1)</mtext></mtd><mtd><mi>f</mi><mo stretchy=&quot;false&quot;>(</mo><mi>x</mi><mo stretchy=&quot;false&quot;>)</mo><mo>=</mo><msup><mi>x</mi><mn>2</mn></msup></mtd></mlabeledtr></mtable></math>" role="presentation"></span></div>

<script type="math/tex; mode=display" id="MathJax-Element-3">\begin{equation} f(x) = x^2 \end{equation}</script>

<div class="highlight-wrap">

<figure class="highlight tex">

<div class="table-container">

<table>

<tbody>

<tr>

<td class="gutter">

<pre><span class="line">1</span>  
<span class="line">2</span>  
<span class="line">3</span>  
<span class="line">4</span>  
<span class="line">5</span>  
</pre>

</td>

<td class="code">

<pre><span class="line"><span class="formula">$</span></span>  
<span class="line"><span class="formula"><span class="tag">\<span class="name">begin</span><span class="string">{equation}</span></span></span></span>  
<span class="line"><span class="formula">f(x) = x^2</span></span>  
<span class="line"><span class="formula"><span class="tag">\<span class="name">end</span><span class="string">{equation}</span></span></span></span>  
<span class="line"><span class="formula">$</span></span>  
</pre>

</td>

</tr>

</tbody>

</table>

</div>

</figure>

<div class="copy-btn">复制</div>

</div>

### [](#公式组 "公式组")公式组

使用 `\begin{eqnarray}…\end{eqnarray}` 来添加一组公式。例如

<span class="MathJax_Preview" style="color: inherit;"></span>

<div class="MathJax_Display has-jax"><span class="MathJax MathJax_FullWidth" id="MathJax-Element-4-Frame" tabindex="0" style="position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot; display=&quot;block&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-41" style="width: 100%; display: inline-block; min-width: 8.205em;"><span style="display: inline-block; position: relative; width: 100%; height: 0px; font-size: 129%; min-width: 8.205em;"><span style="position: absolute; clip: rect(2.426em, 1004.05em, 5.084em, -1000em); top: -4.005em; left: 0em; width: 100%;"><span class="mrow" id="MathJax-Span-42"><span class="mtable" id="MathJax-Span-43" style="min-width: 8.205em;"><span style="display: inline-block; position: relative; width: 100%; height: 0px; min-width: 8.205em;"><span style="display: inline-block; position: absolute; width: 4.049em; height: 0px; clip: rect(-1.579em, 1004.05em, 1.079em, -1000em); top: 0em; left: 50%; margin-left: -2.024em;"><span style="position: absolute; clip: rect(2.785em, 1000.51em, 4.834em, -1000em); top: -4.005em; left: 0em;"><span style="display: inline-block; position: relative; width: 0.529em; height: 0px;"><span style="position: absolute; clip: rect(3.435em, 1000.51em, 4.144em, -1000em); top: -4.655em; right: 0em;"><span class="mtd" id="MathJax-Span-47"><span class="mrow" id="MathJax-Span-48"><span class="mi" id="MathJax-Span-49" style="font-family: MathJax_Math-italic;">a</span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; clip: rect(3.876em, 1000em, 4.134em, -1000em); top: -3.305em; right: 0em;"><span class="mtd" id="MathJax-Span-62"><span class="mrow" id="MathJax-Span-63"></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; clip: rect(2.859em, 1001em, 4.834em, -1000em); top: -4.005em; left: 0.529em;"><span style="display: inline-block; position: relative; width: 1.056em; height: 0px;"><span style="position: absolute; clip: rect(3.509em, 1001em, 4.134em, -1000em); top: -4.655em; left: 50%; margin-left: -0.528em;"><span class="mtd" id="MathJax-Span-50"><span class="mrow" id="MathJax-Span-51"><span class="mi" id="MathJax-Span-52"></span><span class="mo" id="MathJax-Span-53" style="font-family: MathJax_Main; padding-left: 0.278em;">=</span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; clip: rect(3.509em, 1001em, 4.134em, -1000em); top: -3.305em; left: 50%; margin-left: -0.528em;"><span class="mtd" id="MathJax-Span-64"><span class="mrow" id="MathJax-Span-65"><span class="mi" id="MathJax-Span-66"></span><span class="mo" id="MathJax-Span-67" style="font-family: MathJax_Main; padding-left: 0.278em;">=</span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; clip: rect(2.532em, 1002.19em, 5.039em, -1000em); top: -4.005em; left: 1.863em;"><span style="display: inline-block; position: relative; width: 2.186em; height: 0px;"><span style="position: absolute; clip: rect(3.182em, 1002.08em, 4.216em, -1000em); top: -4.655em; left: 0em;"><span class="mtd" id="MathJax-Span-54"><span class="mrow" id="MathJax-Span-55"><span class="mi" id="MathJax-Span-56" style="font-family: MathJax_Math-italic;">b</span><span class="mo" id="MathJax-Span-57" style="font-family: MathJax_Main; padding-left: 0.222em;">+</span><span class="mi" id="MathJax-Span-58" style="font-family: MathJax_Math-italic; padding-left: 0.222em;">c</span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; clip: rect(3.293em, 1002.19em, 4.339em, -1000em); top: -3.305em; left: 0em;"><span class="mtd" id="MathJax-Span-68"><span class="mrow" id="MathJax-Span-69"><span class="mi" id="MathJax-Span-70" style="font-family: MathJax_Math-italic;">y<span style="display: inline-block; overflow: hidden; height: 1px; width: 0.006em;"></span></span><span class="mo" id="MathJax-Span-71" style="font-family: MathJax_Main; padding-left: 0.222em;">−</span><span class="mi" id="MathJax-Span-72" style="font-family: MathJax_Math-italic; padding-left: 0.222em;">z<span style="display: inline-block; overflow: hidden; height: 1px; width: 0.003em;"></span></span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span><span style="display: inline-block; position: absolute; width: 1.278em; height: 0px; clip: rect(-1.529em, 1001.18em, 1.079em, -1000em); top: 0em; right: 0em; margin-right: 0em;"><span style="position: absolute; clip: rect(3.126em, 1001.18em, 4.384em, -1000em); top: -4.655em; right: 0em;"><span class="mtd" id="mjx-eqn-2"><span class="mrow" id="MathJax-Span-45"><span class="mtext" id="MathJax-Span-46" style="font-family: MathJax_Main;">(2)</span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; clip: rect(3.126em, 1001.18em, 4.384em, -1000em); top: -3.305em; right: 0em;"><span class="mtd" id="mjx-eqn-3"><span class="mrow" id="MathJax-Span-60"><span class="mtext" id="MathJax-Span-61" style="font-family: MathJax_Main;">(3)</span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span></span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -1.281em; border-left: 0px solid; width: 0px; height: 3.207em;"></span></span></nobr><span class="MJX_Assistive_MathML MJX_Assistive_MathML_Block" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mtable columnalign="right center left" rowspacing="3pt" columnspacing="0 thickmathspace" displaystyle="true"><mlabeledtr><mtd id="mjx-eqn-2"><mtext>(2)</mtext></mtd><mtd><mi>a</mi></mtd><mtd><mo>=</mo></mtd><mtd><mi>b</mi><mo>+</mo><mi>c</mi></mtd></mlabeledtr><mlabeledtr><mtd id="mjx-eqn-3"><mtext>(3)</mtext></mtd><mtd><mo>=</mo></mtd><mtd><mi>y</mi><mo>−</mo><mi>z</mi></mtd></mlabeledtr></mtable></math></span><mtable columnalign=&quot;right center left&quot; rowspacing=&quot;3pt&quot; columnspacing=&quot;0 thickmathspace&quot; displaystyle=&quot;true&quot;><mlabeledtr><mtd id=&quot;mjx-eqn-2&quot;><mtext>(2)</mtext></mtd><mtd><mi>a</mi></mtd><mtd><mi></mi><mo>=</mo></mtd><mtd><mi>b</mi><mo>+</mo><mi>c</mi></mtd></mlabeledtr><mlabeledtr><mtd id=&quot;mjx-eqn-3&quot;><mtext>(3)</mtext></mtd><mtd /><mtd><mi></mi><mo>=</mo></mtd><mtd><mi>y</mi><mo>&amp;#x2212;</mo><mi>z</mi></mtd></mlabeledtr></mtable></math>" role="presentation"></span></div>

<script type="math/tex; mode=display" id="MathJax-Element-4">\begin{eqnarray} a & = & b + c \\ & = & y - z \end{eqnarray}</script>

<div class="highlight-wrap">

<figure class="highlight tex">

<div class="table-container">

<table>

<tbody>

<tr>

<td class="gutter">

<pre><span class="line">1</span>  
<span class="line">2</span>  
<span class="line">3</span>  
<span class="line">4</span>  
<span class="line">5</span>  
<span class="line">6</span>  
</pre>

</td>

<td class="code">

<pre><span class="line"><span class="formula">$</span></span>  
<span class="line"><span class="formula"><span class="tag">\<span class="name">begin</span><span class="string">{eqnarray}</span></span></span></span>  
<span class="line"><span class="formula">a & = & b + c <span class="tag">\<span class="name">\</span></span></span></span>  
<span class="line"> <span class="formula">& = & y - z</span></span>  
<span class="line"><span class="formula"><span class="tag">\<span class="name">end</span><span class="string">{eqnarray}</span></span></span></span>  
<span class="line"><span class="formula">$</span></span>  
</pre>

</td>

</tr>

</tbody>

</table>

</div>

</figure>

<div class="copy-btn">复制</div>

</div>

### [](#无数字索引 "无数字索引")无数字索引

在 `equation` 或 `eqnarray` 后加 `*`。例如 `\begin{equation*}` 或 `\begin{eqnarray*}`。

<span class="MathJax_Preview" style="color: inherit;"></span>

<div class="MathJax_Display has-jax" style="text-align: center;"><span class="MathJax" id="MathJax-Element-5-Frame" tabindex="0" style="text-align: center; position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot; display=&quot;block&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-73" style="width: 5.472em; display: inline-block;"><span style="display: inline-block; position: relative; width: 4.22em; height: 0px; font-size: 129%;"><span style="position: absolute; clip: rect(1.399em, 1004.22em, 2.791em, -1000em); top: -2.412em; left: 0em;"><span class="mrow" id="MathJax-Span-74"><span class="mi" id="MathJax-Span-75" style="font-family: MathJax_Math-italic;">f<span style="display: inline-block; overflow: hidden; height: 1px; width: 0.06em;"></span></span><span class="mo" id="MathJax-Span-76" style="font-family: MathJax_Main;">(</span><span class="mi" id="MathJax-Span-77" style="font-family: MathJax_Math-italic;">x</span><span class="mo" id="MathJax-Span-78" style="font-family: MathJax_Main;">)</span><span class="mo" id="MathJax-Span-79" style="font-family: MathJax_Main; padding-left: 0.278em;">=</span><span class="msubsup" id="MathJax-Span-80" style="padding-left: 0.278em;"><span style="display: inline-block; position: relative; width: 1.001em; height: 0px;"><span style="position: absolute; clip: rect(3.434em, 1000.52em, 4.145em, -1000em); top: -4.005em; left: 0em;"><span class="mi" id="MathJax-Span-81" style="font-family: MathJax_Math-italic;">x</span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; top: -4.418em; left: 0.572em;"><span class="mn" id="MathJax-Span-82" style="font-size: 70.7%; font-family: MathJax_Main;">2</span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span></span></span><span style="display: inline-block; width: 0px; height: 2.412em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.378em; border-left: 0px solid; width: 0px; height: 1.574em;"></span></span></nobr><span class="MJX_Assistive_MathML MJX_Assistive_MathML_Block" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mi>f</mi><mo stretchy="false">(</mo><mi>x</mi><mo stretchy="false">)</mo><mo>=</mo><msup><mi>x</mi><mn>2</mn></msup></math></span><mi>f</mi><mo stretchy=&quot;false&quot;>(</mo><mi>x</mi><mo stretchy=&quot;false&quot;>)</mo><mo>=</mo><msup><mi>x</mi><mn>2</mn></msup></math>" role="presentation"></span></div>

<script type="math/tex; mode=display" id="MathJax-Element-5">\begin{equation*} f(x) = x ^ 2 \end{equation*}</script>

<div class="highlight-wrap">

<figure class="highlight tex">

<div class="table-container">

<table>

<tbody>

<tr>

<td class="gutter">

<pre><span class="line">1</span>  
<span class="line">2</span>  
<span class="line">3</span>  
<span class="line">4</span>  
<span class="line">5</span>  
</pre>

</td>

<td class="code">

<pre><span class="line"><span class="formula">$</span></span>  
<span class="line"><span class="formula"><span class="tag">\<span class="name">begin</span><span class="string">{equation*}</span></span></span></span>  
<span class="line"><span class="formula">f(x) = x ^ 2</span></span>  
<span class="line"><span class="formula"><span class="tag">\<span class="name">end</span><span class="string">{equation*}</span></span></span></span>  
<span class="line"><span class="formula">$</span></span>  
</pre>

</td>

</tr>

</tbody>

</table>

</div>

</figure>

<div class="copy-btn">复制</div>

</div>

### [](#公式索引和引用 "公式索引和引用")公式索引和引用

使用 `\label{tag}` 来给公式加上数字引用标签。

<span class="MathJax_Preview" style="color: inherit;"></span>

<div class="MathJax_Display has-jax" style="text-align: center;"><span class="MathJax" id="MathJax-Element-6-Frame" tabindex="0" style="text-align: center; position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot; display=&quot;block&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-83" style="width: 4.567em; display: inline-block;"><span style="display: inline-block; position: relative; width: 3.531em; height: 0px; font-size: 129%;"><span style="position: absolute; clip: rect(1.399em, 1003.53em, 2.552em, -1000em); top: -2.412em; left: 0em;"><span class="mrow" id="MathJax-Span-84"><span class="mi" id="MathJax-Span-85" style="font-family: MathJax_Math-italic;">e</span><span class="mo" id="MathJax-Span-86" style="font-family: MathJax_Main; padding-left: 0.278em;">=</span><span class="mi" id="MathJax-Span-87" style="font-family: MathJax_Math-italic; padding-left: 0.278em;">m</span><span class="msubsup" id="MathJax-Span-88"><span style="display: inline-block; position: relative; width: 0.862em; height: 0px;"><span style="position: absolute; clip: rect(3.434em, 1000.43em, 4.145em, -1000em); top: -4.005em; left: 0em;"><span class="mi" id="MathJax-Span-89" style="font-family: MathJax_Math-italic;">c</span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; top: -4.418em; left: 0.433em;"><span class="mn" id="MathJax-Span-90" style="font-size: 70.7%; font-family: MathJax_Main;">2</span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span></span></span><span style="display: inline-block; width: 0px; height: 2.412em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.07em; border-left: 0px solid; width: 0px; height: 1.265em;"></span></span></nobr><span class="MJX_Assistive_MathML MJX_Assistive_MathML_Block" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mi>e</mi><mo>=</mo><mi>m</mi><msup><mi>c</mi><mn>2</mn></msup></math></span><mi>e</mi><mo>=</mo><mi>m</mi><msup><mi>c</mi><mn>2</mn></msup></math>" role="presentation"></span></div>

<script type="math/tex; mode=display" id="MathJax-Element-6">e = mc^2 \label{eq1}</script>

<div class="highlight-wrap">

<figure class="highlight plain">

<div class="table-container">

<table>

<tbody>

<tr>

<td class="gutter">

<pre><span class="line">1</span>  
<span class="line">2</span>  
<span class="line">3</span>  
</pre>

</td>

<td class="code">

<pre><span class="line">$</span>  
<span class="line">e = mc^2 \label{eq1}</span>  
<span class="line">$</span>  
</pre>

</td>

</tr>

</tbody>

</table>

</div>

</figure>

<div class="copy-btn">复制</div>

</div>

使用 `\eqref(tag)` 来指向引用的公式。例如：这是爱因斯坦的公式<span class="MathJax_Preview" style="color: inherit;"></span><span class="MathJax" id="MathJax-Element-7-Frame" tabindex="0" style="position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-91" style="width: 1.854em; display: inline-block;"><span style="display: inline-block; position: relative; width: 1.421em; height: 0px; font-size: 129%;"><span style="position: absolute; clip: rect(1.534em, 1001.37em, 2.498em, -1000em); top: -2.369em; left: 0em;"><span class="mrow" id="MathJax-Span-92">[<span class="mrow MathJax_ref" id="MathJax-Span-93"><span class="mtext" id="MathJax-Span-94" style="font-family: MathJax_Main;">???</span></span>](#)</span><span style="display: inline-block; width: 0px; height: 2.369em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.056em; border-left: 0px solid; width: 0px; height: 1.021em;"></span></span></nobr><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow class="MathJax_ref" href="#"><mtext>???</mtext></mrow></math></span><mrow class=&quot;MathJax_ref&quot; href=&quot;#&quot;><mtext>???</mtext></mrow></math>" role="presentation"></span><script type="math/tex" id="MathJax-Element-7">\ref{eq1}</script>。

<div class="highlight-wrap">

<figure class="highlight plain">

<div class="table-container">

<table>

<tbody>

<tr>

<td class="gutter">

<pre><span class="line">1</span>  
</pre>

</td>

<td class="code">

<pre><span class="line">这是爱因斯坦的公式$\ref{eq1}$。</span>  
</pre>

</td>

</tr>

</tbody>

</table>

</div>

</figure>

<div class="copy-btn">复制</div>

</div>

在多行公式中使用 `\nonumber` 来省略数字引用标签。

<span class="MathJax_Preview" style="color: inherit;"></span>

<div class="MathJax_Display has-jax"><span class="MathJax MathJax_FullWidth" id="MathJax-Element-8-Frame" tabindex="0" style="position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot; display=&quot;block&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-95" style="width: 100%; display: inline-block; min-width: 8.28em;"><span style="display: inline-block; position: relative; width: 100%; height: 0px; font-size: 129%; min-width: 8.28em;"><span style="position: absolute; clip: rect(2.448em, 1004.08em, 5.062em, -1000em); top: -4.005em; left: 0em; width: 100%;"><span class="mrow" id="MathJax-Span-96"><span class="mtable" id="MathJax-Span-97" style="min-width: 8.28em;"><span style="display: inline-block; position: relative; width: 100%; height: 0px; min-width: 8.28em;"><span style="display: inline-block; position: absolute; width: 4.124em; height: 0px; clip: rect(-1.557em, 1004.08em, 1.057em, -1000em); top: 0em; left: 50%; margin-left: -2.062em;"><span style="position: absolute; clip: rect(2.665em, 1002.29em, 5.017em, -1000em); top: -4.005em; left: 0em;"><span style="display: inline-block; position: relative; width: 2.29em; height: 0px;"><span style="position: absolute; clip: rect(3.293em, 1002.29em, 4.339em, -1000em); top: -4.633em; right: 0em;"><span class="mtd" id="MathJax-Span-98"><span class="mrow" id="MathJax-Span-99"><span class="mi" id="MathJax-Span-100" style="font-family: MathJax_Math-italic;">x</span><span class="mo" id="MathJax-Span-101" style="font-family: MathJax_Main; padding-left: 0.222em;">+</span><span class="mi" id="MathJax-Span-102" style="font-family: MathJax_Math-italic; padding-left: 0.222em;">y<span style="display: inline-block; overflow: hidden; height: 1px; width: 0.006em;"></span></span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; clip: rect(3.293em, 1002.29em, 4.339em, -1000em); top: -3.328em; right: 0em;"><span class="mtd" id="MathJax-Span-111"><span class="mrow" id="MathJax-Span-112"><span class="mi" id="MathJax-Span-113" style="font-family: MathJax_Math-italic;">x</span><span class="mo" id="MathJax-Span-114" style="font-family: MathJax_Main; padding-left: 0.222em;">−</span><span class="mi" id="MathJax-Span-115" style="font-family: MathJax_Math-italic; padding-left: 0.222em;">y<span style="display: inline-block; overflow: hidden; height: 1px; width: 0.006em;"></span></span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; clip: rect(2.582em, 1001.79em, 4.834em, -1000em); top: -4.005em; left: 2.29em;"><span style="display: inline-block; position: relative; width: 1.834em; height: 0px;"><span style="position: absolute; clip: rect(3.21em, 1001.76em, 4.134em, -1000em); top: -4.633em; left: 0em;"><span class="mtd" id="MathJax-Span-103"><span class="mrow" id="MathJax-Span-104"><span class="mi" id="MathJax-Span-105"></span><span class="mo" id="MathJax-Span-106" style="font-family: MathJax_Main; padding-left: 0.278em;">=</span><span class="mn" id="MathJax-Span-107" style="font-family: MathJax_Main; padding-left: 0.278em;">1</span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span><span style="position: absolute; clip: rect(3.21em, 1001.79em, 4.156em, -1000em); top: -3.328em; left: 0em;"><span class="mtd" id="MathJax-Span-116"><span class="mrow" id="MathJax-Span-117"><span class="mi" id="MathJax-Span-118"></span><span class="mo" id="MathJax-Span-119" style="font-family: MathJax_Main; padding-left: 0.278em;">=</span><span class="mn" id="MathJax-Span-120" style="font-family: MathJax_Main; padding-left: 0.278em;">0</span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span><span style="display: inline-block; position: absolute; width: 1.278em; height: 0px; clip: rect(-0.202em, 1001.18em, 1.057em, -1000em); top: 0em; right: 0em; margin-right: 0em;"><span style="position: absolute; clip: rect(3.126em, 1001.18em, 4.384em, -1000em); top: -3.328em; right: 0em;"><span class="mtd" id="mjx-eqn-eq2"><span class="mrow" id="MathJax-Span-109"><span class="mtext" id="MathJax-Span-110" style="font-family: MathJax_Main;">(4)</span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span></span></span></span><span style="display: inline-block; width: 0px; height: 4.005em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -1.252em; border-left: 0px solid; width: 0px; height: 3.149em;"></span></span></nobr><span class="MJX_Assistive_MathML MJX_Assistive_MathML_Block" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mtable columnalign="right left right left right left right left right left right left" rowspacing="3pt" columnspacing="0em 2em 0em 2em 0em 2em 0em 2em 0em 2em 0em" displaystyle="true"><mtr><mtd><mi>x</mi><mo>+</mo><mi>y</mi></mtd><mtd><mo>=</mo><mn>1</mn></mtd></mtr><mlabeledtr><mtd id="mjx-eqn-eq2"><mtext>(4)</mtext></mtd><mtd><mi>x</mi><mo>−</mo><mi>y</mi></mtd><mtd><mo>=</mo><mn>0</mn></mtd></mlabeledtr></mtable></math></span><mtable columnalign=&quot;right left right left right left right left right left right left&quot; rowspacing=&quot;3pt&quot; columnspacing=&quot;0em 2em 0em 2em 0em 2em 0em 2em 0em 2em 0em&quot; displaystyle=&quot;true&quot;><mtr><mtd><mi>x</mi><mo>+</mo><mi>y</mi></mtd><mtd><mi></mi><mo>=</mo><mn>1</mn></mtd></mtr><mlabeledtr><mtd id=&quot;mjx-eqn-eq2&quot;><mtext>(4)</mtext></mtd><mtd><mi>x</mi><mo>&amp;#x2212;</mo><mi>y</mi></mtd><mtd><mi></mi><mo>=</mo><mn>0</mn></mtd></mlabeledtr></mtable></math>" role="presentation"></span></div>

<script type="math/tex; mode=display" id="MathJax-Element-8">\begin{align} x + y &= 1 \nonumber \\ x - y &= 0 \label{eq2} \end{align}</script>

<div class="highlight-wrap">

<figure class="highlight plain">

<div class="table-container">

<table>

<tbody>

<tr>

<td class="gutter">

<pre><span class="line">1</span>  
<span class="line">2</span>  
<span class="line">3</span>  
<span class="line">4</span>  
</pre>

</td>

<td class="code">

<pre><span class="line">\begin{align}</span>  
<span class="line">x + y &= 1 \nonumber \\</span>  
<span class="line">x - y &= 0 \label{eq2}</span>  
<span class="line">\end{align}</span>  
</pre>

</td>

</tr>

</tbody>

</table>

</div>

</figure>

<div class="copy-btn">复制</div>

</div>

## [](#常用语法 "常用语法")常用语法

<div class="table-container">

<div class="table-container">

<table>

<thead>

<tr>

<th style="text-align:center">名称</th>

<th style="text-align:center">公式</th>

<th style="text-align:center">语法</th>

</tr>

</thead>

<tbody>

<tr>

<td style="text-align:center">上标/幂</td>

<td style="text-align:center" class="has-jax"><span class="MathJax_Preview" style="color: inherit;"></span><span class="MathJax" id="MathJax-Element-9-Frame" tabindex="0" style="position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-121" style="width: 5.678em; display: inline-block;"><span style="display: inline-block; position: relative; width: 4.281em; height: 0px; font-size: 132%;"><span style="position: absolute; clip: rect(1.379em, 1004.28em, 2.695em, -1000em); top: -2.357em; left: 0em;"><span class="mrow" id="MathJax-Span-122"><span class="msubsup" id="MathJax-Span-123"><span style="display: inline-block; position: relative; width: 1.001em; height: 0px;"><span style="position: absolute; clip: rect(3.406em, 1000.52em, 4.148em, -1000em); top: -3.992em; left: 0em;"><span class="mi" id="MathJax-Span-124" style="font-family: MathJax_Math-italic;">x</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; top: -4.355em; left: 0.572em;"><span class="mn" id="MathJax-Span-125" style="font-size: 70.7%; font-family: MathJax_Main;">2</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span></span></span><span class="mo" id="MathJax-Span-126" style="font-family: MathJax_Main;">,</span><span class="msubsup" id="MathJax-Span-127" style="padding-left: 0.167em;"><span style="display: inline-block; position: relative; width: 0.999em; height: 0px;"><span style="position: absolute; clip: rect(3.182em, 1000.45em, 4.137em, -1000em); top: -3.992em; left: 0em;"><span class="mn" id="MathJax-Span-128" style="font-family: MathJax_Main;">2</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; top: -4.385em; left: 0.5em;"><span class="mi" id="MathJax-Span-129" style="font-size: 70.7%; font-family: MathJax_Math-italic;">n</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span></span></span><span class="mo" id="MathJax-Span-130" style="font-family: MathJax_Main;">,</span><span class="msubsup" id="MathJax-Span-131" style="padding-left: 0.167em;"><span style="display: inline-block; position: relative; width: 1.382em; height: 0px;"><span style="position: absolute; clip: rect(3.406em, 1000.58em, 4.148em, -1000em); top: -3.992em; left: 0em;"><span class="mi" id="MathJax-Span-132" style="font-family: MathJax_Math-italic;">n</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; top: -4.355em; left: 0.6em;"><span class="texatom" id="MathJax-Span-133"><span class="mrow" id="MathJax-Span-134"><span class="mn" id="MathJax-Span-135" style="font-size: 70.7%; font-family: MathJax_Main;">22</span></span></span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span></span></span></span><span style="display: inline-block; width: 0px; height: 2.357em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.32em; border-left: 0px solid; width: 0px; height: 1.484em;"></span></span></nobr><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>x</mi><mn>2</mn></msup><mo>,</mo><msup><mn>2</mn><mi>n</mi></msup><mo>,</mo><msup><mi>n</mi><mrow class="MJX-TeXAtom-ORD"><mn>22</mn></mrow></msup></math></span><msup><mi>x</mi><mn>2</mn></msup><mo>,</mo><msup><mn>2</mn><mi>n</mi></msup><mo>,</mo><msup><mi>n</mi><mrow class=&quot;MJX-TeXAtom-ORD&quot;><mn>22</mn></mrow></msup></math>" role="presentation"></span><script type="math/tex" id="MathJax-Element-9">x^2, 2^n, n^{22}</script></td>

<td style="text-align:center">`x^2, 2^n, n^{22}`</td>

</tr>

<tr>

<td style="text-align:center">下标</td>

<td style="text-align:center" class="has-jax"><span class="MathJax_Preview" style="color: inherit;"></span><span class="MathJax" id="MathJax-Element-10-Frame" tabindex="0" style="position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-136" style="width: 1.782em; display: inline-block;"><span style="display: inline-block; position: relative; width: 1.347em; height: 0px; font-size: 132%;"><span style="position: absolute; clip: rect(1.772em, 1001.35em, 2.795em, -1000em); top: -2.357em; left: 0em;"><span class="mrow" id="MathJax-Span-137"><span class="msubsup" id="MathJax-Span-138"><span style="display: inline-block; position: relative; width: 1.336em; height: 0px;"><span style="position: absolute; clip: rect(3.407em, 1000.51em, 4.147em, -1000em); top: -3.992em; left: 0em;"><span class="mi" id="MathJax-Span-139" style="font-family: MathJax_Math-italic;">a</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; top: -3.842em; left: 0.529em;"><span class="texatom" id="MathJax-Span-140"><span class="mrow" id="MathJax-Span-141"><span class="mi" id="MathJax-Span-142" style="font-size: 70.7%; font-family: MathJax_Math-italic;">i</span><span class="mo" id="MathJax-Span-143" style="font-size: 70.7%; font-family: MathJax_Main;">,</span><span class="mi" id="MathJax-Span-144" style="font-size: 70.7%; font-family: MathJax_Math-italic;">j</span></span></span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span></span></span></span><span style="display: inline-block; width: 0px; height: 2.357em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.452em; border-left: 0px solid; width: 0px; height: 1.098em;"></span></span></nobr><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>a</mi><mrow class="MJX-TeXAtom-ORD"><mi>i</mi><mo>,</mo><mi>j</mi></mrow></msub></math></span><msub><mi>a</mi><mrow class=&quot;MJX-TeXAtom-ORD&quot;><mi>i</mi><mo>,</mo><mi>j</mi></mrow></msub></math>" role="presentation"></span><script type="math/tex" id="MathJax-Element-10">a_{i, j}</script></td>

<td style="text-align:center">`a_{i, j}`</td>

</tr>

<tr>

<td style="text-align:center">分数</td>

<td style="text-align:center" class="has-jax"><span class="MathJax_Preview" style="color: inherit;"></span><span class="MathJax" id="MathJax-Element-11-Frame" tabindex="0" style="position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-145" style="width: 3.177em; display: inline-block;"><span style="display: inline-block; position: relative; width: 2.405em; height: 0px; font-size: 132%;"><span style="position: absolute; clip: rect(1.139em, 1002.41em, 2.887em, -1000em); top: -2.357em; left: 0em;"><span class="mrow" id="MathJax-Span-146"><span class="mfrac" id="MathJax-Span-147"><span style="display: inline-block; position: relative; width: 0.474em; height: 0px; margin-right: 0.12em; margin-left: 0.12em;"><span style="position: absolute; clip: rect(3.377em, 1000.32em, 4.137em, -1000em); top: -4.392em; left: 50%; margin-left: -0.177em;"><span class="mn" id="MathJax-Span-148" style="font-size: 70.7%; font-family: MathJax_Main;">2</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; clip: rect(3.378em, 1000.32em, 4.152em, -1000em); top: -3.622em; left: 50%; margin-left: -0.177em;"><span class="mn" id="MathJax-Span-149" style="font-size: 70.7%; font-family: MathJax_Main;">3</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; clip: rect(0.854em, 1000.47em, 1.203em, -1000em); top: -1.278em; left: 0em;"><span style="display: inline-block; overflow: hidden; vertical-align: 0em; border-top: 1.3px solid; width: 0.474em; height: 0px;"></span><span style="display: inline-block; width: 0px; height: 1.058em;"></span></span></span></span><span class="mo" id="MathJax-Span-150" style="font-family: MathJax_Main;">,</span><span class="msubsup" id="MathJax-Span-151" style="padding-left: 0.167em;"><span style="display: inline-block; position: relative; width: 1.257em; height: 0px;"><span style="position: absolute; clip: rect(3.406em, 1000.52em, 4.148em, -1000em); top: -3.992em; left: 0em;"><span class="mi" id="MathJax-Span-152" style="font-family: MathJax_Math-italic;">x</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; top: -4.406em; left: 0.572em;"><span class="mfrac" id="MathJax-Span-153"><span style="display: inline-block; position: relative; width: 0.37em; height: 0px; margin-right: 0.12em; margin-left: 0.12em;"><span style="position: absolute; clip: rect(3.515em, 1000.21em, 4.137em, -1000em); top: -4.319em; left: 50%; margin-left: -0.125em;"><span class="mn" id="MathJax-Span-154" style="font-size: 50%; font-family: MathJax_Main;">1</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; clip: rect(3.515em, 1000.23em, 4.137em, -1000em); top: -3.686em; left: 50%; margin-left: -0.125em;"><span class="mn" id="MathJax-Span-155" style="font-size: 50%; font-family: MathJax_Main;">2</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; clip: rect(0.854em, 1000.37em, 1.203em, -1000em); top: -1.205em; left: 0em;"><span style="display: inline-block; overflow: hidden; vertical-align: 0em; border-top: 1.3px solid; width: 0.37em; height: 0px;"></span><span style="display: inline-block; width: 0px; height: 1.058em;"></span></span></span></span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span></span></span></span><span style="display: inline-block; width: 0px; height: 2.357em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.573em; border-left: 0px solid; width: 0px; height: 2.054em;"></span></span></nobr><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mn>2</mn><mn>3</mn></mfrac><mo>,</mo><msup><mi>x</mi><mfrac><mn>1</mn><mn>2</mn></mfrac></msup></math></span><mfrac><mn>2</mn><mn>3</mn></mfrac><mo>,</mo><msup><mi>x</mi><mfrac><mn>1</mn><mn>2</mn></mfrac></msup></math>" role="presentation"></span><script type="math/tex" id="MathJax-Element-11">\frac{2}{3}, x^\frac{1}{2}</script></td>

<td style="text-align:center">`\frac{2}{3}, x^\frac{1}{2}`</td>

</tr>

<tr>

<td style="text-align:center">开方</td>

<td style="text-align:center" class="has-jax"><span class="MathJax_Preview" style="color: inherit;"></span><span class="MathJax" id="MathJax-Element-12-Frame" tabindex="0" style="position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-156" style="width: 4.139em; display: inline-block;"><span style="display: inline-block; position: relative; width: 3.127em; height: 0px; font-size: 132%;"><span style="position: absolute; clip: rect(1.355em, 1003.13em, 2.695em, -1000em); top: -2.357em; left: 0em;"><span class="mrow" id="MathJax-Span-157"><span class="msqrt" id="MathJax-Span-158"><span style="display: inline-block; position: relative; width: 1.333em; height: 0px;"><span style="position: absolute; clip: rect(3.182em, 1000.45em, 4.137em, -1000em); top: -3.992em; left: 0.833em;"><span class="mrow" id="MathJax-Span-159"><span class="mn" id="MathJax-Span-160" style="font-family: MathJax_Main;">2</span></span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; clip: rect(3.563em, 1000.5em, 3.889em, -1000em); top: -4.565em; left: 0.833em;"><span style="font-family: MathJax_Main;">–</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; clip: rect(3.048em, 1000.85em, 4.337em, -1000em); top: -4.04em; left: 0em;"><span style="font-family: MathJax_Main;">√</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span></span></span><span class="mo" id="MathJax-Span-161" style="font-family: MathJax_Main;">,</span><span class="mroot" id="MathJax-Span-162" style="padding-left: 0.167em;"><span style="display: inline-block; position: relative; width: 1.333em; height: 0px;"><span style="position: absolute; clip: rect(3.183em, 1000.46em, 4.159em, -1000em); top: -3.992em; left: 0.833em;"><span class="mn" id="MathJax-Span-163" style="font-family: MathJax_Main;">3</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; clip: rect(3.563em, 1000.5em, 3.889em, -1000em); top: -4.553em; left: 0.833em;"><span style="font-family: MathJax_Main;">–</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; clip: rect(3.048em, 1000.85em, 4.337em, -1000em); top: -4.029em; left: 0em;"><span style="font-family: MathJax_Main;">√</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; clip: rect(3.627em, 1000.29em, 4.142em, -1000em); top: -4.474em; left: 0.251em;"><span class="mi" id="MathJax-Span-164" style="font-size: 50%; font-family: MathJax_Math-italic;">n</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span></span></span></span><span style="display: inline-block; width: 0px; height: 2.357em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.32em; border-left: 0px solid; width: 0px; height: 1.515em;"></span></span></nobr><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><msqrt><mn>2</mn></msqrt><mo>,</mo><mroot><mn>3</mn><mi>n</mi></mroot></math></span><msqrt><mn>2</mn></msqrt><mo>,</mo><mroot><mn>3</mn><mi>n</mi></mroot></math>" role="presentation"></span><script type="math/tex" id="MathJax-Element-12">\sqrt{2}, \sqrt[n]{3}</script></td>

<td style="text-align:center">`\sqrt{2}, \sqrt[n]{3}`</td>

</tr>

<tr>

<td style="text-align:center">无穷大</td>

<td style="text-align:center" class="has-jax"><span class="MathJax_Preview" style="color: inherit;"></span><span class="MathJax" id="MathJax-Element-13-Frame" tabindex="0" style="position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-165" style="width: 5.293em; display: inline-block;"><span style="display: inline-block; position: relative; width: 3.992em; height: 0px; font-size: 132%;"><span style="position: absolute; clip: rect(1.63em, 1003.94em, 2.695em, -1000em); top: -2.357em; left: 0em;"><span class="mrow" id="MathJax-Span-166"><span class="mo" id="MathJax-Span-167" style="font-family: MathJax_Main;">+</span><span class="mi" id="MathJax-Span-168" style="font-family: MathJax_Main;">∞</span><span class="mo" id="MathJax-Span-169" style="font-family: MathJax_Main;">,</span><span class="mo" id="MathJax-Span-170" style="font-family: MathJax_Main; padding-left: 0.167em;">−</span><span class="mi" id="MathJax-Span-171" style="font-family: MathJax_Main;">∞</span></span><span style="display: inline-block; width: 0px; height: 2.357em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.32em; border-left: 0px solid; width: 0px; height: 1.153em;"></span></span></nobr><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><mo>+</mo><mi mathvariant="normal">∞</mi><mo>,</mo><mo>−</mo><mi mathvariant="normal">∞</mi></math></span><mo>+</mo><mi mathvariant=&quot;normal&quot;>&amp;#x221E;</mi><mo>,</mo><mo>&amp;#x2212;</mo><mi mathvariant=&quot;normal&quot;>&amp;#x221E;</mi></math>" role="presentation"></span><script type="math/tex" id="MathJax-Element-13">+\infty, -\infty</script></td>

<td style="text-align:center">`+\infty, -\infty`</td>

</tr>

<tr>

<td style="text-align:center">极限</td>

<td style="text-align:center" class="has-jax"><span class="MathJax_Preview" style="color: inherit;"></span><span class="MathJax" id="MathJax-Element-14-Frame" tabindex="0" style="position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-172" style="width: 10.536em; display: inline-block;"><span style="display: inline-block; position: relative; width: 7.985em; height: 0px; font-size: 132%;"><span style="position: absolute; clip: rect(1.463em, 1007.95em, 3.259em, -1000em); top: -2.357em; left: 0em;"><span class="mrow" id="MathJax-Span-173"><span class="munderover" id="MathJax-Span-174"><span style="display: inline-block; position: relative; width: 2.369em; height: 0px;"><span style="position: absolute; clip: rect(3.154em, 1001.38em, 4.137em, -1000em); top: -3.992em; left: 0.49em;"><span class="mo" id="MathJax-Span-175" style="font-family: MathJax_Main;">lim</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; clip: rect(3.436em, 1002.33em, 4.295em, -1000em); top: -3.392em; left: 0em;"><span class="texatom" id="MathJax-Span-176"><span class="mrow" id="MathJax-Span-177"><span class="mi" id="MathJax-Span-178" style="font-size: 70.7%; font-family: MathJax_Math-italic;">x</span><span class="mo" id="MathJax-Span-179" style="font-size: 70.7%; font-family: MathJax_Main;">→</span><span class="mo" id="MathJax-Span-180" style="font-size: 70.7%; font-family: MathJax_Main;">+</span><span class="mi" id="MathJax-Span-181" style="font-size: 70.7%; font-family: MathJax_Main;">∞</span></span></span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span></span></span><span class="mi" id="MathJax-Span-182" style="font-family: MathJax_Main; padding-left: 0.167em;">exp</span><span class="mo" id="MathJax-Span-183"></span><span class="mo" id="MathJax-Span-184" style="font-family: MathJax_Main;">(</span><span class="mo" id="MathJax-Span-185" style="font-family: MathJax_Main;">−</span><span class="mi" id="MathJax-Span-186" style="font-family: MathJax_Math-italic;">x</span><span class="mo" id="MathJax-Span-187" style="font-family: MathJax_Main;">)</span><span class="mo" id="MathJax-Span-188" style="font-family: MathJax_Main; padding-left: 0.278em;">=</span><span class="mn" id="MathJax-Span-189" style="font-family: MathJax_Main; padding-left: 0.278em;">0</span></span><span style="display: inline-block; width: 0px; height: 2.357em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -1.064em; border-left: 0px solid; width: 0px; height: 2.118em;"></span></span></nobr><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><munder><mo form="prefix">lim</mo><mrow class="MJX-TeXAtom-ORD"><mi>x</mi><mo stretchy="false">→</mo><mo>+</mo><mi mathvariant="normal">∞</mi></mrow></munder><mi>exp</mi><mo>⁡</mo><mo stretchy="false">(</mo><mo>−</mo><mi>x</mi><mo stretchy="false">)</mo><mo>=</mo><mn>0</mn></math></span><munder><mo form=&quot;prefix&quot;>lim</mo><mrow class=&quot;MJX-TeXAtom-ORD&quot;><mi>x</mi><mo stretchy=&quot;false&quot;>&amp;#x2192;</mo><mo>+</mo><mi mathvariant=&quot;normal&quot;>&amp;#x221E;</mi></mrow></munder><mi>exp</mi><mo>&amp;#x2061;</mo><mo stretchy=&quot;false&quot;>(</mo><mo>&amp;#x2212;</mo><mi>x</mi><mo stretchy=&quot;false&quot;>)</mo><mo>=</mo><mn>0</mn></math>" role="presentation"></span><script type="math/tex" id="MathJax-Element-14">\lim \limits _{x \to +\infty} \exp(-x) = 0</script></td>

<td style="text-align:center">`\lim \limits _{x \to +\infty} \exp(-x) = 0`</td>

</tr>

<tr>

<td style="text-align:center">对数</td>

<td style="text-align:center" class="has-jax"><span class="MathJax_Preview" style="color: inherit;"></span><span class="MathJax" id="MathJax-Element-15-Frame" tabindex="0" style="position: relative;" data-mathml="<math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;><nobr aria-hidden="true"><span class="math" id="MathJax-Span-190" style="width: 11.595em; display: inline-block;"><span style="display: inline-block; position: relative; width: 8.754em; height: 0px; font-size: 132%;"><span style="position: absolute; clip: rect(1.463em, 1008.66em, 2.751em, -1000em); top: -2.357em; left: 0em;"><span class="mrow" id="MathJax-Span-191"><span class="mi" id="MathJax-Span-192" style="font-family: MathJax_Main;">log</span><span class="mo" id="MathJax-Span-193"></span><span class="mo" id="MathJax-Span-194" style="font-family: MathJax_Main;">(</span><span class="mi" id="MathJax-Span-195" style="font-family: MathJax_Math-italic;">n</span><span class="mo" id="MathJax-Span-196" style="font-family: MathJax_Main;">)</span><span class="mo" id="MathJax-Span-197" style="font-family: MathJax_Main;">,</span><span class="msubsup" id="MathJax-Span-198" style="padding-left: 0.167em;"><span style="display: inline-block; position: relative; width: 1.707em; height: 0px;"><span style="position: absolute; clip: rect(3.154em, 1001.26em, 4.343em, -1000em); top: -3.992em; left: 0em;"><span class="mi" id="MathJax-Span-199" style="font-family: MathJax_Main;">log</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span><span style="position: absolute; top: -3.751em; left: 1.278em;"><span class="mn" id="MathJax-Span-200" style="font-size: 70.7%; font-family: MathJax_Main;">2</span><span style="display: inline-block; width: 0px; height: 3.992em;"></span></span></span></span><span class="mo" id="MathJax-Span-201"></span><span class="mo" id="MathJax-Span-202" style="font-family: MathJax_Main;">(</span><span class="mi" id="MathJax-Span-203" style="font-family: MathJax_Math-italic;">n</span><span class="mo" id="MathJax-Span-204" style="font-family: MathJax_Main;">)</span><span class="mo" id="MathJax-Span-205" style="font-family: MathJax_Main;">,</span><span class="mi" id="MathJax-Span-206" style="font-family: MathJax_Main; padding-left: 0.167em;">ln</span><span class="mo" id="MathJax-Span-207"></span><span class="mo" id="MathJax-Span-208" style="font-family: MathJax_Main;">(</span><span class="mi" id="MathJax-Span-209" style="font-family: MathJax_Math-italic;">x</span><span class="mo" id="MathJax-Span-210" style="font-family: MathJax_Main;">)</span></span><span style="display: inline-block; width: 0px; height: 2.357em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.393em; border-left: 0px solid; width: 0px; height: 1.447em;"></span></span></nobr><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>log</mi><mo>⁡</mo><mo stretchy="false">(</mo><mi>n</mi><mo stretchy="false">)</mo><mo>,</mo><msub><mi>log</mi><mn>2</mn></msub><mo>⁡</mo><mo stretchy="false">(</mo><mi>n</mi><mo stretchy="false">)</mo><mo>,</mo><mi>ln</mi><mo>⁡</mo><mo stretchy="false">(</mo><mi>x</mi><mo stretchy="false">)</mo></math></span><mi>log</mi><mo>&amp;#x2061;</mo><mo stretchy=&quot;false&quot;>(</mo><mi>n</mi><mo stretchy=&quot;false&quot;>)</mo><mo>,</mo><msub><mi>log</mi><mn>2</mn></msub><mo>&amp;#x2061;</mo><mo stretchy=&quot;false&quot;>(</mo><mi>n</mi><mo stretchy=&quot;false&quot;>)</mo><mo>,</mo><mi>ln</mi><mo>&amp;#x2061;</mo><mo stretchy=&quot;false&quot;>(</mo><mi>x</mi><mo stretchy=&quot;false&quot;>)</mo></math>" role="presentation"></span><script type="math/tex" id="MathJax-Element-15">\log(n), \log_2(n), \ln(x)</script></td>

<td style="text-align:center">`\log(n), \log_2(n), \ln(x)`</td>

</tr>

</tbody>

</table>

</div>

</div>

更多语法，查看这篇文章：[LaTeX 数学公式语法](/201902/latex-syntax-for-math-equation)

## [](#参考链接 "参考链接")参考链接

*   [LaTeX](https://zh.wikipedia.org/wiki/LaTeX), Wikipedia.
*   [MathJax](https://zh.wikipedia.org/wiki/MathJax), Wikipedia.
*   [LATEX Math for Undergrads](http://tug.ctan.org/info/undergradmath/undergradmath.pdf), Jim Hefferon, Saint Michael’s College, VT USA.
*   [LATEX for Beginners](http://www.docs.is.ed.ac.uk/skills/documents/3722/3722-2014.pdf), University of Edinburgh.
*   [LaTeX/Mathematics](https://en.wikibooks.org/wiki/LaTeX/Mathematics), Wikibooks;
*   [markdown 数学公式Latex语法](https://juejin.im/post/5af93ec6518825428b38e7f4), by wangzhengquan.

</div>
