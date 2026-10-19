# Name Mangler

# Mangle the name by reversing it or borgifying it
def modified_name(name, add_borg):
    # Split the name into first and last in a list
    split_name = name.split()

    # Reverse the list of name components so the list is [last, first]
    reversed_name_components = list(reversed(split_name))

    # Rejoin the list of name components
    new_name1 = ' '.join(reversed_name_components)

    if add_borg:
        # Split the reversed name back into a list
        split_name2 = new_name1.split()

        # Reverse it again so the list is back to [first, last]
        reversed_name_components2 = list(reversed(split_name2))

        # Add Borg to the end of the list
        reversed_name_components2.append("Borg")

        # Rejoin the list of name components
        new_name2 = ' '.join(reversed_name_components2)
        return new_name2

    return new_name1


name = "Johanna Jackson"

print(f"New name: {modified_name(name, False)}")
print(f"New borg name: {modified_name(name, True)}")