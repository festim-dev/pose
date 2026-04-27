import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def plot_europe(ax, s, locations, world_gdf, proj):
    """Plot Europe zoom in the inset axes"""
    # Set the extent to focus on Europe
    # [-10, 30, 35, 70]
    ax.set_extent([-10, 30, 35, 70], crs=ccrs.PlateCarree())

    # Plot the world boundaries
    world_gdf.boundary.plot(ax=ax)

    # Transform coordinates and plot data points
    pc = ccrs.PlateCarree()
    new_coords = proj.transform_points(pc, locations.geometry.x, locations.geometry.y)

    ax.scatter(
        new_coords[:, 0],
        new_coords[:, 1],
        s=s,  # size of the bubbles
        zorder=10,  # this specifies to put bubbles on top of the map
        alpha=0.7,
        color="C1",
        edgecolors="C0",
        linewidth=1,
    )


def plot_locations(locations, pc, proj, **kwargs):
    new_coords = proj.transform_points(pc, locations.geometry.x, locations.geometry.y)
    plt.scatter(x=new_coords[:, 0], y=new_coords[:, 1], **kwargs)
