# Looping batched transfer and delete

A sample flow that demonstrates while-loop-style looping in a flow.

The contents of a given source path are transferred in batches of 100 items,
and are then deleted from the source path.

> [!NOTE]
>
> The sample flow does not validate the results of the transfer and delete tasks.
>
> Even if a transfer task fails, the flow will attempt to delete the batch of items.
> This could lead to data loss.
>
> Even if a delete task fails, the flow will continue to loop
> if there are still items to transfer in the source path.
> This could lead to an infinite loop.
