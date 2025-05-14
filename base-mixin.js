/**
 * @fileoverview check usage of UU5.Common.BaseMixin
 * @author Martin Farkaš
 */
"use strict";

//------------------------------------------------------------------------------
// Rule Definition
//------------------------------------------------------------------------------
const Selectors = require("../core/selectors");

module.exports = {
  meta: {
    type: "problem",
    fixable: "code",
    docs: {
      description: "check usage of UU5.Common.BaseMixin",
      category: "uu5 Supportability",
      recommended: true,
      url:
        "https://uuos9.plus4u.net/uu-bookkitg01-main/78462435-0238a88bac124b3ca828835b57144ffa/book/page?code=uu5BaseMixin"
    },
    messages: {
      baseMixinIsMissing: "UU5 component does not have UU5.Common.BaseMixin"
    }
  },

  create: function(context) {
    const MIXIN_REGEXP = /^mixins$/;
    const BASE_MIXIN_REGEXP = /[[, ](UU5\.Common\.BaseMixin)[\], ]/;

    //----------------------------------------------------------------------
    // Helpers
    //----------------------------------------------------------------------

    function checkRule(context, node) {
      const mixinsProp = node.properties.find(prop => {
        return prop.key.name.match(MIXIN_REGEXP);
      });

      if (!mixinsProp) {
        context.report({
          messageId: "baseMixinIsMissing",
          loc: node.parent.loc
        });
        return;
      }

      const src = context.getSourceCode().getText(mixinsProp);

      if (!src.match(BASE_MIXIN_REGEXP)) {
        context.report({
          messageId: "baseMixinIsMissing",
          loc: mixinsProp.loc
        });
      }
    }

    //----------------------------------------------------------------------
    // Public
    //----------------------------------------------------------------------

    return {
      [Selectors.getCreateReactClassSelector()]: node => checkRule(context, node),
      [Selectors.getVsComponentCreateSelector()]: node => Selectors.checkVsComponent(context, node, checkRule)
    };
  }
};
