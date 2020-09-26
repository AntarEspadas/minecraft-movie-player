# minecraft-movie-player
A series of python scripts that allow the generation of a datapack that plays videos in minecraft

## How it works
The most important part of the script is that which analyses an image pixel by pixel and finds which Minecraft block is the closest in colour. In order to so, the script requires a list of of Minecraft blocks and their average RGB value, this list is known as a palette. The larger the palette, the better the image
## How to create a palette
The script is able to analyse a folder containing minecraft texture images (obtained by extracting .minecraft/versions/[version number]/[version number].jar with any tool such as Winrar or 7Zip) in order to find their average colours and put them on a file, the palette. However, average colour is not all the information the program needs, it also has to know which block IDs go with which colours, and in some cases some NBT data indicating the direction a block is facing.
This information is stored in a file formatted with tab separated values called the index, which tells the script the filenames of different Minecraft blocks, their block IDs and, optionally, the NBT data required to make the block face the right direction.
For example, the following is the file containing the texture for dirt:
![images/dirt.png](placeholder)
The name of this image is dirt.png.
This block is simple enough, as its filename is the same as its block ID and looks the same on all sides. Its corresponding entry on the index would look something like this:

    dirt.png	dirt

However, it is not so simple for other blocks. Consider the following image:
![oak_log_top.png](images/oak_log_top.png)
The name of this image is oak_log_top.png, however its block ID is simply oak_log. Moreover, this block is placed upright by default, meaning we need to add information about its orientation to be able to see the top when standing in front of it. More precisely, the script wants the information required to make its blocks face north.
So, what do we do? We go into Minecraft an place down an oak log facing north with the help of the debug menu (f3), like so:
![oak_log_top.png](images/oak_log_top.png)
Then, we point at the block and look at the right of the debug menu, there, we will find its block ID, as well as information regarding its orientation
![oak_2.png](images/oak_2.png)
The first highlighted line, minecraft:oark_log, is the block ID, the second, axis: z, is the information we need about the orientation, meaning the index would now look like this:

    dirt.png	dirt
    oak_log_top.png	oak_log	{axis:z}
  
Keep in mind that two entries may share the same block ID, so long as they point at different images, for instance, the following entries are fine:
  

    dirt.png	dirt
    oak_log_top.png	oak_log	{axis:z}
    oak_log.png	oak_log	{axis:y}

If we were to add, say, furnaces into the mix, the index would now look like this:

    dirt.png	dirt
    oak_log_top.png	oak_log	{axis:z}
    oak_log.png	oak_log	{axis:y}
    furnace_front.png	furnace	{facing:north}
    furnace_side.png	furnace	{facing:east}
    furnace_back.png	furnace	{facing:south}

Once the index is filled to your own satisfaction, it can be fed into the script to generate the palette

This project comes with its own index and palette, however, they may be incomplete or outdated, so it is encouraged to make a pull request if you have indexed any new blocks.
It is recommended that you don't use any blocks that aren't full blocks, can't stand on their own, would cause light updates (transparent blocks or light emitting blocks), can not be seen at a distance, or would behave in destructive ways (water, lava, TNT)
Feel free to use these blocks at your own risk, but I will be declining any pull requests containing them.
