# Tips

通过Path推挤Shape创建一个Volumn。Shape、Path、Volumn都是理论上的概念。CG graph中的modules创建的Shape、Path、Volumn、VMesh都是数据而已，没有可视化的表示，直到Create模块创建真正的Mesh才能看见真正创建的网格。

Build模块创建的都是理论数据，包括Shape、Path、Volumn、VMesh。Create模块创建真正的资源

Shape+Path **build** Volumn，Volumn **build** VMesh，VMesh **create** Mesh

Shape Extrusion模块从Shape+Path创建Volumn，Path选项调整沿path的栅格化，Cross选项调整沿着横截面的栅格化。Resolution控制栅格化的细分程度。Path选项的Optimize默认优化沿Path的栅格化，但是如果细分程度过低，可以取消此选项，就可以通过Resolution更精细地细化沿着Path的栅格化
