import re
from copy import deepcopy
from jsonschema_serialize_fork import _utils, _validators
from jsonschema_serialize_fork.compat import iteritems
from jsonschema_serialize_fork.exceptions import ValidationError


NO_DEFAULT = object()
REPLACEMENTS = {}


def replaces(validator):
    def decorate(serializer):
        REPLACEMENTS[validator] = serializer
        return serializer
    return decorate


@replaces(_validators.patternProperties)
def patternProperties(validator, patternProperties, instance, schema):
    if not validator.is_type(instance, "object"):
        return

    if validator._serialize:
        validated_instance = validator._validated[-1]

    for pattern, subschema in iteritems(patternProperties):
        for k, v in iteritems(instance):
            if validator._serialize:
                lv = len(validator._validated)
            if re.search(pattern, k):
                for error in validator.descend(
                        v, subschema, path=k, schema_path=pattern
                ):
                    yield error
                if validator._serialize:
                    validated_instance[k] = validator._validated[lv]
                    del validator._validated[lv:]


@replaces(_validators.additionalProperties)
def additionalProperties(validator, aP, instance, schema):
    if not validator.is_type(instance, "object"):
        return

    extras = list(_utils.find_additional_properties(instance, schema))

    if not extras:
        return

    if validator._serialize:
        validated_instance = validator._validated[-1]

    if validator.is_type(aP, "object"):
        for extra in extras:
            if validator._serialize:
                lv = len(validator._validated)
            for error in validator.descend(instance[extra], aP, path=extra):
                yield error
            if validator._serialize:
                validated_instance[extra] = validator._validated[lv]
                del validator._validated[lv:]

    elif not aP:
        error = "Additional properties are not allowed (%s %s unexpected)"
        yield ValidationError(error % _utils.extras_msg(extras))
    elif validator._serialize:
        for extra in extras:
            validated_instance[extra] = deepcopy(instance[extra])


@replaces(_validators.items)
def items(validator, items, instance, schema):
    if not validator.is_type(instance, "array"):
        return

    if validator._serialize:
        validated_instance = validator._validated[-1]

    if validator.is_type(items, "object"):
        for index, item in enumerate(instance):
            if validator._serialize:
                lv = len(validator._validated)
            for error in validator.descend(item, items, path=index):
                yield error
            if validator._serialize:
                validated_instance.append(validator._validated[lv])
                del validator._validated[lv:]
    else:
        for (index, item), subschema in zip(enumerate(instance), items):
            if validator._serialize:
                lv = len(validator._validated)
            for error in validator.descend(
                    item, subschema, path=index, schema_path=index
            ):
                yield error
            if validator._serialize:
                validated_instance.append(validator._validated[lv])
                del validator._validated[lv:]


@replaces(_validators.additionalItems)
def additionalItems(validator, aI, instance, schema):
    if (
        not validator.is_type(instance, "array") or
        validator.is_type(schema.get("items", {}), "object")
    ):
        return

    if validator._serialize:
        validated_instance = validator._validated[-1]

    if validator.is_type(aI, "object"):
        for index, item in enumerate(instance[len(schema.get("items", [])):]):
            if validator._serialize:
                lv = len(validator._validated)
            for error in validator.descend(item, aI, path=index):
                yield error
            if validator._serialize:
                validated_instance.append(validator._validated[lv])
                del validator._validated[lv:]
    elif len(instance) > len(schema.get("items", [])):
        if not aI:
            error = "Additional items are not allowed (%s %s unexpected)"
            yield ValidationError(
                error %
                _utils.extras_msg(instance[len(schema.get("items", [])):])
            )
        elif validator._serialize:
            for item in instance[len(schema.get("items", [])):]:
                validated_instance.append(deepcopy(item))


@replaces(_validators.properties_draft3)
def properties_draft3(validator, properties, instance, schema):
    if not validator.is_type(instance, "object"):
        return

    if validator._serialize:
        validated_instance = validator._validated[-1]

    for property, subschema in iteritems(properties):
        if property in instance:
            if validator._serialize:
                lv = len(validator._validated)
            for error in validator.descend(
                instance[property],
                subschema,
                path=property,
                schema_path=property,
            ):
                yield error
            if validator._serialize:
                validated_instance[property] = validator._validated[lv]
                del validator._validated[lv:]
        else:
            if validator._serialize:
                if "default" in subschema:
                    validated_instance[property] = deepcopy(subschema["default"])
                if "serverDefault" in subschema:
                    default = validator.server_default(property, subschema)
                    if default is not NO_DEFAULT:
                        validated_instance[property] = default
            if subschema.get("required", False):
                error = ValidationError("%r is a required property" % property)
                error._set(
                    validator="required",
                    validator_value=subschema["required"],
                    instance=instance,
                    schema=schema,
                )
                error.path.appendleft(property)
                error.schema_path.extend([property, "required"])
                yield error


@replaces(_validators.properties_draft4)
def properties_draft4(validator, properties, instance, schema):
    if not validator.is_type(instance, "object"):
        return

    if validator._serialize:
        validated_instance = validator._validated[-1]

    for property, subschema in iteritems(properties):
        if property in instance:
            if validator._serialize:
                lv = len(validator._validated)
            for error in validator.descend(
                instance[property],
                subschema,
                path=property,
                schema_path=property,
                # XXX serialize=True,
            ):
                yield error
            if validator._serialize:
                validated_instance[property] = validator._validated[lv]
                del validator._validated[lv:]
        elif validator._serialize:
            if "default" in subschema:
                validated_instance[property] = deepcopy(subschema["default"])
            if "serverDefault" in subschema:
                default = validator.server_default(property, subschema)
                if default is not NO_DEFAULT:
                    validated_instance[property] = default
